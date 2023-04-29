from django.urls import path
from . import views


urlpatterns = [
    path('get-balance', views.get_balance)
]
