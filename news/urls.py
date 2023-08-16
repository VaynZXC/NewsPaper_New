from django.urls import path
from news.views import PostDetail, PostsList, Posts, PostCreate, PostDelete, PostUpdate

app_name = 'NewsPaper'
urlpatterns = [
    path('', PostsList.as_view(), name = 'allnews'),
    path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('news/', Posts.as_view()),
    path('news/create', PostCreate.as_view(),  name='news_create'),
    path('news/update/<int:pk>', PostUpdate.as_view(),  name='news_update'),
    path('news/delete/<int:pk>', PostDelete.as_view(),  name='news_delete'),
]
