from django.urls import path, include
from .views import courses_view
from .api import urls

urlpatterns = [
    path('', courses_view),
    path('api/', include(urls))
]
