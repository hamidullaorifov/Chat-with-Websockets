import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Chat,CustomUser,Message

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#     def disconnect(self, code):
#         return super().disconnect(code)
#     def receive(self, text_data=None, bytes_data=None):
#         print('Textdata',text_data)
#         text_data = json.loads(text_data)
#         message = text_data.get('message','Default Message')
#         self.send(text_data=json.dumps({'message':message}))

    
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        self.room_group_name = f'chat_user_{user.id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()
    

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json["message"]
        sender_id = int(text_data_json['sender_id'])
        chat_id = int(text_data_json['chat_id'])
        sender = await self.get_user(sender_id)
        chat,receiver = await self.get_chat_data(chat_id,sender_id)
        print(receiver,chat)
        message_obj = await self.create_message(sender,chat,message)
        room_group_name = f'chat_user_{receiver.id}'
        response = {
            'message': message,
            'sender_id':sender_id,
            'receiver_id':receiver.id,
            'chat_id':chat_id

        }
        await self.channel_layer.group_send(
            room_group_name,
            {
                "type": "chat_message",
                "response": json.dumps(response)
            }
        )

    @database_sync_to_async
    def get_chat_data(self,pk,sender_id):
        qs = Chat.objects.filter(pk=pk)
        if qs.exists():
            chat = qs.first()
        else:
            chat = None
        if chat:
            receiver = chat.first_user if chat.second_user.id==sender_id else chat.second_user
        return chat,receiver
    @database_sync_to_async
    def create_message(self,sender,chat,message):
        # sender = CustomUser.objects.get(pk=sender_id)
        # chat = Chat.objects.get(pk=chat_id)
        print(sender)
        return Message.objects.create(
            chat = chat,
            text = message,
            sender = sender
            )

    async def chat_message(self, event):
        response = event["response"]

        # Send message to WebSocket
        await self.send(text_data=response)
    @database_sync_to_async
    def get_user(self,pk):
        return CustomUser.objects.get(pk=pk)