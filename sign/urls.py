from django.urls import path
from .views import RegisterView, LoginView, LogoutView

app_name = 'SignApp'
urlpatterns = [
   path('login/', LoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('signup/', RegisterView.as_view(), name='signup')
]