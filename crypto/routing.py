from django.urls import path
from courses.api.consumers import CoursesConsumer

web_sockets_urlpatterns = [
    path('ws/courses/get-courses', CoursesConsumer.as_asgi()),
]
