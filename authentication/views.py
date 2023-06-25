from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from . import services

import json
from .forms import CustomUserCreationForm, LogInForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': True})
        else:
            errors = json.loads(form.errors.as_json())
            return JsonResponse({'errors': errors,'success': False})
    else:
        form = CustomUserCreationForm
        return render(
            request, 
            'authentication/register.html',
            context={'form': form})


def auth(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            user=authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': False})
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = LogInForm()
            return render(
                request=request, 
                template_name="authentication/login.html",
                context={'form': form})


def lk(request):
    return render(
                request=request, 
                template_name="authentication/lk.html",
                context={'currencies': services.get_user_data(request.user), 'lk': True})
