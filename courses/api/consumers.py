from channels.generic.websocket import AsyncWebsocketConsumer


class CoursesConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sending_task = None

    async def connect(self):
        await self.channel_layer.group_add('courses', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard('courses', self.channel_name)

    async def send_courses(self, event):
        await self.send(text_data=event["text"])
