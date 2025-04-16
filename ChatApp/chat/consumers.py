import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Ticket, Message

class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.room_group_name = f'ticket_{self.ticket_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_name = data['sender_name']

        # 🔽 Save the message to DB
        ticket = await database_sync_to_async(Ticket.objects.get)(id=self.ticket_id)
        await database_sync_to_async(Message.objects.create)(
            ticket=ticket,
            sender_name=sender_name,
            message=message
        )

        # 🔁 Broadcast to others
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_name': sender_name
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_name': event['sender_name']
        }))
