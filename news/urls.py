from django.urls import path
from news.views import PostDetail, PostsList, Posts, PostCreate, PostDelete, PostUpdate, ProfileView, ConfirmationView, upgrade_me, subscribe

app_name = 'NewsPaper'
urlpatterns = [
    path('', PostsList.as_view(), name = 'allnews'),
    path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('news/', Posts.as_view()),
    path('news/create', PostCreate.as_view(),  name='news_create'),
    path('news/update/<int:pk>', PostUpdate.as_view(),  name='news_update'),
    path('news/delete/<int:pk>', PostDelete.as_view(),  name='news_delete'),
    path('account/profile.html', ProfileView.as_view(), name='profile'),
    path('account/upgrade.html', upgrade_me, name='upgrade'),

    # Категории
    path('categories/<int:pk>', subscribe, name='subscribe'),
    path('categories/subscribe.html', ConfirmationView.as_view(), name='confirmation' )
]
