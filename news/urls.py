from django.urls import path
from news.views import PostDetail, PostsList, Posts, PostCreate, PostDelete, PostUpdate

app_name = 'allnews'
urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('news/', Posts.as_view(), name='news'),
    path('news/create', PostCreate.as_view()),
    path('news/update/<int:pk>', PostUpdate.as_view()),
    path('news/delete/<int:pk>', PostDelete.as_view()),
]
