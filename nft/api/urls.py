from django.urls import path
from . import views

urlpatterns = [
    path('get-marketplace-posts', views.marketplace),
    path('get-collections', views.collections),
    path('get-user-nft', views.user_nft),
    path('get-collections-list', views.get_collections_list),
    path('nft-info/<int:nft_id>', views.nft_info),
    path('sell-nft', views.sell_nft),
    path('marketplace-post-info/<int:post_id>', views.post_info),
    path('add-nft', views.add_nft),
    path('buy-nft', views.buy_nft)
]
