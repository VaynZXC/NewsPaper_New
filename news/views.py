from django.shortcuts import render
from django.views.generic import ListView, DetailView
from news.models import Post

# Create your views here.
class PostsList(ListView):
    model = Post
    template_name = 'news/allnews.html'
    context_object_name = 'allNews'
    queryset = Post.objects.order_by('-id')

class PostDetail(DetailView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'