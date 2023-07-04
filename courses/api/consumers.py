from channels.generic.websocket import WebsocketConsumer
from pprint import pprint

class CoursesConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send('123')
        pprint(self.__dict__)
        print(self.scope['user'])

    def receive(self, text_data=None, bytes_data=None):
        print('recived:', text_data)

    def disconnect(self, code):
        print('disconnected')
