from django.urls import path
from .views import home
from django.contrib.auth.decorators import login_required

app_name = 'blog'
urlpatterns = [
    path('', login_required(home), name='home')
]
