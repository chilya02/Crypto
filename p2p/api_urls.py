from django.urls import path
from . import api_views

urlpatterns = [
    path('get-buy-list/<str:section>', api_views.get_buy_list),
    path('get-sell-list/<str:section>', api_views.get_sell_list),
    path('get-posts-list/<str:section>', api_views.get_posts_list),
    path('get-orders-list', api_views.get_orders_list),
    path('get-buy-info/<int:post_id>', api_views.get_buy_post_info),
    path('get-sell-info/<int:post_id>', api_views.get_sell_post_info),
    path('get-post-info/<str:section>/<int:post_id>', api_views.get_my_post_info),
    path('get-new-order-info/<int:order_id>', api_views.get_new_order_info),
    path('get-currency-count/<str:currency>', api_views.get_user_currency_count),
    path('add-post', api_views.add_post),
    path('send-message', api_views.send_message),
    path('create-order', api_views.create_order),
    path('get-messages/<int:order_id>', api_views.get_messages),
    path('get-messages-interface/<int:order_id>', api_views.get_messages_interface),
    path('get-p2p-interface', api_views.get_p2p_interface),
    path('change-order-count/<int:order_id>', api_views.change_order_count),
    path('pay-order', api_views.pay_order),
    path('add-card-number', api_views.add_card_number),
    path('delete-post', api_views.delete_post),
    path('close-order', api_views.close_order),
    path('abort-order', api_views.abort_order),
]
