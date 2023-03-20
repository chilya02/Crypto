from django.contrib import admin
from .models import BuyPost, SellPost, NewOrder, Order, Message
# Register your models here.
@admin.register(SellPost)
class SellPostAdmin(admin.ModelAdmin):
    list_display = ("user", "currency", "price", "limit")

@admin.register(BuyPost)
class BuyPostAdmin(admin.ModelAdmin):
    list_display = ("user", "currency", "price", "limit")

@admin.register(NewOrder)
class NewOrderAdmin(admin.ModelAdmin):
    list_display = ("buyer", "seller", "post_type")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("from_user", "order")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("currency", "buyer", "seller",  "sum", "count")