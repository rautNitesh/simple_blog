from django.urls import path
from .views import UserLoginView, UserCreateView, UserLogoutView, UserDetailView


app_name = 'accounts'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('details/<int:pk>', UserDetailView.as_view(), name='details')
]
