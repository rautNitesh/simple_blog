from django.urls import path
from .views import BlogListView
from django.contrib.auth.decorators import login_required

app_name = 'blog'
urlpatterns = [
    path('', login_required(BlogListView.as_view()), name='home')
]
