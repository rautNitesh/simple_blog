from django.urls import path
from .views import UserLoginView, UserCreateView, UserLogoutView, UserDetailView, UserUpdateView, UserDeleteView, UserEmailValidateView


app_name = 'accounts'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('details/<int:pk>', UserDetailView.as_view(), name='details'),
    path('details/<int:pk>/update', UserUpdateView.as_view(), name='update'),
    path('details/<int:pk>/delete', UserDeleteView.as_view(), name='delete'),
    path('details/<int:pk>/validate', UserEmailValidateView.as_view(), name='validate_mail'),
]
