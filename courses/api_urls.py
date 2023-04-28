from django.urls import path
from .views import courses_view
from . import api_urls

urlpatterns = [
    path('', courses_view),
]

