from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST

from user.forms import RegistrationForm, LoginForm
from user.auth import EmailBackend


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, 'Thank you for registering')
            return HttpResponseRedirect(reverse('service:service_list'))
    else:
        form = RegistrationForm()

    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print(1)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=email, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, 'You are now logged in')

            return HttpResponseRedirect(reverse('service:service_list'))
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})


@login_required
def logout_view(request):
    messages.success(request, f'{request.user.username}, You have been logged out')
    auth.logout(request)
    return redirect(reverse('service:service_list'))


class UserPasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy("user:password_change_done")
    template_name = "user/registration/password_change_form.html"


class UserPasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("user:password_reset_done")
    email_template_name = "user/registration/password_reset_email.html"
    template_name = "user/registration/password_reset_form.html"


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "user/registration/password_reset_done.html"


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("user:password_reset_complete")
    template_name = "user/registration/password_reset_confirm.html"


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "user/registration/password_reset_complete.html"


@login_required
def user_dashboard(request):
    return render(request, 'user/dashboard.html')
