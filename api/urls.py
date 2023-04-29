from django.urls import path


from . import views

urlpatterns = [
    path('get-buy-list/<str:section>', views.get_buy_list),
    path('get-sell-list/<str:section>', views.get_sell_list),
    path('get-posts-list/<str:section>', views.get_posts_list),
    path('get-orders-list', views.get_orders_list),
    path('get-buy-info/<int:post_id>', views.get_buy_post_info),
    path('get-sell-info/<int:post_id>', views.get_sell_post_info),
    path('get-post-info/<str:section>/<int:post_id>', views.get_my_post_info),
    path('get-new-order-info/<int:order_id>', views.get_new_order_info),
    path('get-currency-count/<str:currency>', views.get_user_currency_count),
    path('add-post', views.add_post),
    path('send-message', views.send_message),
    path('create-order', views.create_order),
    path('get-messages/<int:order_id>', views.get_messages),
    path('get-messages-interface/<int:order_id>', views.get_messages_interface),
    path('get-p2p-interface', views.get_p2p_interface),
    path('change-order-count/<int:order_id>', views.change_order_count),
    path('pay-order', views.pay_order),
    path('add-card-number', views.add_card_number),
    path('delete-post', views.delete_post),
    path('close-order', views.close_order),
    path('abort-order', views.abort_order),
    path('get-balance', views.get_balance),
]
