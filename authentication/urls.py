from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
from .api import urls
urlpatterns = [
    path('auth', views.auth),
    path('register', views.register),
    path("logout", LogoutView.as_view(), name="logout"),
    path('lk', views.lk),
    path('api/', include(urls))
]
