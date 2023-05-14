from django.urls import path
from . import views

urlpatterns = [
    path('get-marketplace-posts', views.marketplace),
    path('get-collections', views.collections),
    path('get-user-nft', views.user_nft),
    path('get-collections-list', views.get_collections_list)
]
