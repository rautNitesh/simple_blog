from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View, CreateView, UpdateView, DetailView, DeleteView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.core.mail import send_mail

from .forms import UserLoginForm, UserCreateForm, UserUpdateForm
from .models import UserModel


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('blog:home')
    redirect_authenticated_user = True


class UserCreateView(View):

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            raise Http404("You are not allowed to edit this Post")
        return render(request, 'accounts/register.html', {"form": UserCreateForm()})

    def post(self, request, *args, **kwargs):
        form = UserCreateForm()
        import random
        import math
        value = int(math.ceil(random.randint(10000, 100000)))
        body = f" Hey there , this message is sent to {request.POST.get('email')} " \
               f" please verify your account with the following code{value}"
        send_mail(
            'Verify your identity',
            body,
            'from@yourdjangoapp.com',
            ['to@yourbestuser.com'],
            fail_silently=False,
        )
        if request.FILES.get('profile_pic'):
            file = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            _ = file.name.split('.')
            # if _.pop() == "png" or _.pop() == "jpg" or _.pop() == "jpeg":
            fs.save(file.name, file)
            form = UserCreateForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.confirm_code = value
                user.save()
                return HttpResponseRedirect(reverse('accounts:validate_mail', kwargs={'pk': user.pk}))
        return render(request, 'accounts/register.html', {"form": form})


class UserLogoutView(LogoutView):
    template_name = 'accounts/logged_out.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().dispatch(self, *args, **kwargs)
        raise Http404("The page doesn't exist.")


class UserDetailView(DetailView):
    template_name = 'accounts/profile.html'
    pk_url_kwarg = 'pk'
    model = UserModel

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != self.request.user:
            raise Http404("This page doesn't exist")
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'accounts/update_profile.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('blog:home')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user.is_authenticated:
            if obj.email != self.request.user.email:
                raise Http404("The page doesn't exist")
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("The page doesn't exist")

    # def post(self, request, *args, **kwargs):
    #     if request.POST and request.FILES['profile_pic']:
    #         file = request.FILES['profile_pic']
    #         fs = FileSystemStorage()
    #         _ = file.name.split('.')
    #         if _.pop() == "png" or _.pop() == "jpg" or _.pop() == "jpeg":
    #             super().post(request, profile_pic=file.name, *args, **kwargs)
    #             fs.save(file.name, file)
    #
    #     return redirect(reverse_lazy('blog:home'))


class UserDeleteView(DeleteView):
    model = UserModel
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('blog:home')
    template_name = 'accounts/confirm_del.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != self.request.user:
            raise Http404("The page doesn't exist")
        return super().dispatch(request, *args, **kwargs)


class UserEmailValidateView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/validate_mail.html')

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('accounts:profile')
        user_id = self.kwargs['pk']
        user = UserModel.objects.get(pk=user_id)
        print(user)
        print(type(user.confirm_code))
        print(type(request.POST.get('code')))
        if int(user.confirm_code) == int(request.POST.get('code')):
            user.is_active = True
            user.save()
            print(user.is_active)
            return redirect('accounts:login')
        else:
            return redirect('accounts:validate_mail')
