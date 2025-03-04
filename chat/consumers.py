"""
Consumers = View (но для WebSocket)

Consumers — это классы, обрабатывающие события жизненного цикла соединения:
подключение, получение сообщений и отключение.
===========
Channel(канал) = Уникальные адреса для отправки сообщений.
*Каждый Consumer(View) имеет свой Channel(канал)/room(комнату)

Group(группы) = Коллекции каналов под общим именем.
Позволяют отправлять сообщения сразу нескольким Consumers.
"""
import json

from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Вызывается при установке соединения.
        Здесь можно аутентифицировать пользователя."""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        """Вызывается при разрыве соединения.
        Время попрощаться и очистить ресурсы."""
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive messsage from WebSocket
    async def receive(self, text_data):
        """Обрабатывает входящие сообщения от клиента."""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'chat.message', 'message': message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))
