from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import Post, Author, PostCategory, Category
from .filters import PostFilter
from .forms import PostForm

# Create your views here.
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
            sport = Category.objects.get(category=Category.sport)
            obj.category.set([sport])
        return super().get(request, *args, **kwargs)

class PostDetail(DetailView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'

class Posts(View):
   def get(self, request):
      posts = Post.objects.order_by('-id')
      p = Paginator(posts, 10)
      posts = p.get_page(request.GET.get('page', 1))

      data = {
          'posts': posts
         }
      return render(request, 'news/allnews.html', data)
