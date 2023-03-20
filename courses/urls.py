from django.urls import path
from .views import courses_view
urlpatterns = [
    path('', courses_view),
]

