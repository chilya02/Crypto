from django.urls import path

from . import views

urlpatterns = [
    path('marketplace', views.marketplace),
    path('my-nft', views.my_nft),
    path('collections', views.collections),
]