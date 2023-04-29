from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input disabled',
                'oninput': "checkElement('#id_password2', this)"
                }
            )
        )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input disabled',
                'oninput': "checkElement('#id_register', this)"
                }
            )
        )
    username = forms.CharField(
        label='Имя пользователя', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'oninput': "checkElement('#id_email', this)"
                }
            )
        )
    email = forms.EmailField(
        label='email', 
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input disabled',
                'oninput': "checkElement('#id_password1', this)"
                }
            )
        )

    class Meta:

        model = User
        fields = ("username", "email")


class LogInForm(forms.Form):
    
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={
        'class': 'form-input',
        'oninput': "checkElement('#id_password', this)"
        }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-input disabled',
        'oninput': "checkElement('#id_auth', this)"
        }))
