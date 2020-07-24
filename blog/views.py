from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect

from .models import BlogPost
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .forms import BlogForm


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    # queryset = BlogPost.objects.all()[::-1]


class BlogCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/create.html'
    form_class = BlogForm
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/confirm_delete.html'
    success_url = reverse_lazy('blog:home')
    context_object_name = 'post'
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        post_obj = self.get_object()
        if post_obj.user == self.request.user:
            return super(BlogPostDeleteView, self).dispatch(request, *args, **kwargs)
        return Http404("This page is not available")

           
class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/details.html'
    context_object_name = 'post'


class BlogUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogForm
    template_name = 'blog/update.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        raise Http404('The page you requested is not available right now or moved somewhere')







