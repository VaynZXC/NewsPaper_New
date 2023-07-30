from django.urls import path
from news.views import PostDetail, PostsList, Posts
 
 
urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('news/', Posts.as_view())
]
