from django.urls import path
from .views import UserLoginView, UserCreateView


app_name = 'accounts'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='register'),
]
