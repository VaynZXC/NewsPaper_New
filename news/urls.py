from django.urls import path
from news.views import PostDetail, PostsList
 
 
urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
]