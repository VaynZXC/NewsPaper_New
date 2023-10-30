from django.urls import path
from news.views import PostDetail, PostsList, Posts, PostCreate, PostDelete, PostUpdate, ProfileView, ConfirmationView, upgrade_me, subscribe
from news.views import unsubscribe, ConfirmationViewUnsubscribe

from django.views.decorators.cache import cache_page

app_name = 'NewsPaper'
urlpatterns = [
    path('', (PostsList.as_view()), name = 'allnews'),
    path('news/<int:pk>', (PostDetail.as_view()), name='news_detail'),
    path('news/', Posts.as_view()),
    path('news/create', PostCreate.as_view(),  name='news_create'),
    path('news/update/<int:pk>', PostUpdate.as_view(),  name='news_update'),
    path('news/delete/<int:pk>', PostDelete.as_view(),  name='news_delete'),
    path('account/profile', ProfileView.as_view(), name='profile'),
    path('account/upgrade.html', upgrade_me, name='upgrade'),

    # Категории
    path('category/<int:pk>', ConfirmationView.as_view(), name='category'),
    path('category/<int:pk>/subscribe', subscribe, name='subscribe' ),
    path('category/unsubscribe/<int:pk>', ConfirmationViewUnsubscribe.as_view(), name='category_unsubscribe'),
    path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe' ),
]
