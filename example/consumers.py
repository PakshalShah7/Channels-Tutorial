import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print('connect')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join a room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        print('disconnect')
        # Leave a room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        print('receive')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send a message to a room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive a message from a room group
    async def chat_message(self, event):
        message = event['message']

        # Send a message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))
