from crypto.celery import app
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .services import Courses

channel_layer = get_channel_layer()


@app.task
def send_courses():
    data = Courses.get_courses()
    async_to_sync(channel_layer.group_send)('courses', {"type": "send_courses", "text": data, })
