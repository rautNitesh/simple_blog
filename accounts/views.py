from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage

from .forms import UserLoginForm, UserCreateForm
from .models import UserModel


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('blog:home')
    redirect_authenticated_user = True


class UserCreateView(CreateView):
    model = UserModel
    form_class = UserCreateForm
    template_name = 'accounts/register.html'

    def post(self, request, *args, **kwargs):
        if request.FILES['profile_pic']:
            file = request.FILES['profile_pic']
            fs = FileSystemStorage()
            _ = file.name.split('.')
            if _.pop() == "png" or _.pop() == "jpg" or _.pop() =="jpeg":
                super().post(request, profile_pic=file.name, *args, **kwargs)
                fs.save(file.name, file)
        return redirect(reverse_lazy('blog:home'))






    



