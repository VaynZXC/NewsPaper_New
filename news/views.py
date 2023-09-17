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
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from datetime import datetime

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

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    template_name = 'news/news_create.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = Author.objects.get(user=request.user)
            obj.save()
            form.save_m2m()
            return redirect('NewsPaper:news_detail', obj.pk)
        
    def notificate(self, request, pk):
        user = self.request.user
        subscribers = CategorySubscriber.objects.prefetch_related('subscriber').get(id=id)
        for subscriber in subscribers:
            category = subscriber.category_id
            user = subscriber.subscriber_id
            
        
    
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
        context['is_not_author'] = not self.request.user.groups.filter(name = 'author').exists()
        context['is_not_subscriber'] = not self.request.user.groups.filter(name='subscriber').exists()

        user = self.request.user
        categories = CategorySubscriber.objects.filter(subscriber=user.id)
          
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

#@login_required
#def subscribe_me(request):
    user = request.user
    premium_group = Group.objects.get(name='subscriber')
    if not request.user.groups.filter(name='subscriber').exists():
        premium_group.user_set.add(user)
    return redirect('profile.html')

def subscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.add(request.user.id)
    return redirect('NewsPaper:allnews')

def unsubscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user.id)
    return redirect('NewsPaper:allnews')

def sub_category(request, category_id):
    category_id.subscribers.add(request.user.id)
    return redirect('NewsPaper:confirm_subscription')