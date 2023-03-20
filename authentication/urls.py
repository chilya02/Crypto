from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('auth', auth),
    path('register', register),
    path("logout", LogoutView.as_view(), name="logout"),
    path('lk', lk),
]