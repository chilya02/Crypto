from django.urls import path
from . import views
urlpatterns = [
    path('buy', views.buy),
    path('buy/<int:post_id>', views.buy_post),
    path('sell', views.sell),
    path('sell/<int:post_id>', views.sell_post),
    path('my-posts', views.my_posts),
    path('my-posts/<str:section>/<int:post_id>', views.my_post),
    path('my-orders', views.my_orders),
    path('my-orders/<int:order_id>', views.my_order),
    path('my-orders/new/<int:order_id>', views.my_new_order),
]