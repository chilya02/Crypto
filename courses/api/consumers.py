from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from courses.models import get_courses
import json



class CoursesConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sending_task = None

    async def connect(self):
        await self.accept()
        await self.send('123')
        self.sending_task = await asyncio.ensure_future(self.run_periodic_task())


    async def run_periodic_task(self):
        while True:
            data = await get_courses()
            await self.send(json.dumps(data))
            await asyncio.sleep(1)

    def receive(self, text_data=None, bytes_data=None):
        print('recived:', text_data)

    def disconnect(self, code):
        print('disconnected')
        self.sending_task.cancel()
