from django.urls import path, include
from .api import urls
from . import views

urlpatterns = [
    path('api/', include(urls)),
    path('marketplace', views.marketplace),
    path('my-nft', views.my_nft),
    path('collections', views.collections),
]