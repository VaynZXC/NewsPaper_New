from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic import DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Post, Author, Category, CategorySubscriber, User
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta
from django.core.exceptions import PermissionDenied
from django.core.cache import cache

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

class PostsList(ListView):
    model = Post
    template_name = 'news/allnews.html'
    context_object_name = 'allNews'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = Author.objects.get(user=request.user)
            obj.save()
            form.save_m2m()
        return super().get(request, *args, **kwargs)

class PostDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset) 
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

class PostCreate(UserPassesTestMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    template_name = 'news/news_create.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = request.user

        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = Author.objects.get(user=user)  
            obj.save()
            form.save_m2m()
            return redirect('NewsPaper:news_detail', obj.pk)
    
    def test_func(self, *args, **kwargs):
        author = Author.objects.get(user=self.request.user.id)
        yesterday = datetime.now() - timedelta(days=1)
        post_day = Post.objects.filter(author=author, time_in__gt=yesterday).count()
        print(post_day)
        if post_day > 2:
            raise PermissionDenied("Допускается постить до 3 новостей в день")
        else:
            return redirect('NewsPaper:profile')


@method_decorator(login_required(login_url = '/'), name='dispatch')
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    template_name = 'news/news_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    
    success_url = reverse_lazy('NewsPaper:allnews')

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news/news_delete.html'
    context_object_name = 'news'
    queryset = Post.objects.all()
    success_url = reverse_lazy('NewsPaper:allnews')

class Posts(View):
   def get(self, request):
      posts = Post.objects.order_by('-id')
      p = Paginator(posts, 10)
      posts = p.get_page(request.GET.get('page', 1))

      data = {
          'posts': posts
         }
      return render(request, 'news/allnews.html', data)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        author = Author.objects.get(user=user)
        categories = CategorySubscriber.objects.filter(subscriber=user.id)
        yesterday = datetime.now() - timedelta(days=1)

        context['is_not_author'] = not user.groups.filter(name = 'author').exists()
        context['is_not_subscriber'] = not user.groups.filter(name='subscriber').exists()
        context['posts_on_this_day'] = Post.objects.filter(author=author, time_in__gt=yesterday).count()

        if categories:
          context['subscribed'] = True
          context['categories'] = categories
        else:
          context['subscribed'] = False
        return context
    
class ConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'categories/subscribe.html'
    model = Post
    
    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(pk=pk)
        subscribed = category.subscribers.filter(email=user.email)
        if not subscribed:
            context['subscribed'] = True
            context['category'] = category
        else:
            context['subscribed'] = False
            context['category'] = category
        return context

class ConfirmationViewUnsubscribe(LoginRequiredMixin, TemplateView):
    template_name = 'categories/unsubscribe.html'
    model = Post
    
    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=pk)
        context['category'] = category
        return context

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(user)
    return redirect('NewsPaper:profile')

@login_required
def subscribe_me(request):
    user = request.user
    premium_group = Group.objects.get(name='subscriber')
    if not request.user.groups.filter(name='subscriber').exists():
        premium_group.user_set.add(user)
    return redirect('NewsPaper:profile')

def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user.id)
        email = user.email
        html = render_to_string(
            'mail/subscribe.html',
            {
                'category': category,
                'user': user,    
            },
          )
        
        msg = EmailMultiAlternatives(
              subject = f'{category} subscription',
              body = f'Здравствуй, {user}. Новая статья в твоём любимом разделе!',
              from_email = DEFAULT_FROM_EMAIL,
              to = [email, ],
            )
        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect('NewsPaper:profile')
    return redirect('NewsPaper:allnews')
    
def unsubscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user.id)
    return redirect('NewsPaper:allnews')
