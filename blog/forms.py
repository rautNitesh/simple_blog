from django import forms
from .models import BlogPost


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        exclude = ['updated_at', 'created_at', 'slug', 'user']

