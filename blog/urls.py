from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import BlogListView, BlogCreateView, BlogPostDeleteView, BlogDetailView, BlogUpdateView


app_name = 'blog'
urlpatterns = [
    path('', login_required(BlogListView.as_view()), name='home'),
    path('create/', login_required(BlogCreateView.as_view()), name='create'),
    path('delete/<int:pk>', login_required(BlogPostDeleteView.as_view()), name='delete'),
    path('details/<slug:slug>', login_required(BlogDetailView.as_view()), name='details'),
    path('update/<slug:slug>', login_required(BlogUpdateView.as_view()), name='update'),
]
