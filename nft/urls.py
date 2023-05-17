from django.urls import path, include
from .api import urls
from . import views

urlpatterns = [
    path('api/', include(urls)),
    path('marketplace', views.marketplace),
    path('marketplace/<int:post_id>', views.post_info),
    path('my-nft', views.my_nft),
    path('collections', views.collections),
    path('nft-info/<int:nft_id>', views.nft_info),
]