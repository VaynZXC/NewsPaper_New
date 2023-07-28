from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from news.models import Post
from django.utils import timezone
from .filters import PostFilter

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
      return context

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