from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

from .forms import UserLoginForm, UserCreateForm
from .models import UserModel


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('blog:home')
    redirect_authenticated_user = True


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('blog:home')

    def post(self, request, *args, **kwargs):
        if request.FILES['profile_pic']:
            file = request.FILES['profile_pic']
            fs = FileSystemStorage()
            _ = file.name.split('.')
            if _.pop() == "png" or _.pop() == "jpg" or _.pop() == "jpeg":
                super().post(request, profile_pic=file.name, *args, **kwargs)
                fs.save(file.name, file)

        return redirect(reverse_lazy('blog:home'))


class UserLogoutView(LogoutView):
    template_name = 'accounts/logged_out.html'


class UserDetailView(DetailView):
    template_name = 'accounts/profile.html'
    pk_url_kwarg = 'pk'
    model = UserModel

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
    
    
class UserUpdateView(UpdateView):
    pass










    



