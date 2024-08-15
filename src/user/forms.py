from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from user.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_provider = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ('email', 'password')


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()


class EditProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
