from django.shortcuts import redirect, render

from .models import BlogPost
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .forms import BlogForm


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    queryset = BlogPost.objects.all()[::-1]


class BlogCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/create.html'
    form_class = BlogForm

    def post(self, request, *args, **kwargs):
        form = BlogForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = self.request.user
            post.save()
            return redirect('blog:home')
        return render(request, 'blog/create.html', {'form': form})
           






