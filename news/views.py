from django.shortcuts import render
from django.views.generic import ListView, DetailView
from news.models import Post
from django.utils import timezone

# Create your views here.
class PostsList(ListView):
    model = Post
    template_name = 'news/allnews.html'
    context_object_name = 'allNews'
    queryset = Post.objects.order_by('-id')

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['time_now'] = timezone.localtime(timezone.now())
      context['value1'] = None
      return context

class PostDetail(DetailView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'