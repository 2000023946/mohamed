from channels.generic.websocket import AsyncWebsocketConsumer
import json 
from channels.db import database_sync_to_async
from posts.models import Member, Request
class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_name = f'room_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()
        
        await self.send(text_data=json.dumps({
            'status': 'succuess',
            'message':f'New chatter joined {self.room_name}'
        }))
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        await self.close()
        print('disconnected')

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type':'chat.message',
                'data':data
            }
        )
        

    async def chat_message(self, event):
        await self.send(json.dumps((event['data'])))

class RequestConsumer(AsyncWebsocketConsumer):
    usernames = set()
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.request_name = f'request_{self.username}'

        await self.channel_layer.group_add(
            self.request_name,
            self.channel_name
        )

        self.usernames.add(self.username)

        await self.accept()
        print(self.usernames)

    async def disconnect(self, code):
        print(self.usernames)
        self.usernames.discard(self.username)
        print(self.usernames)
        await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data['user']
        if username in self.usernames:
            await self.channel_layer.group_send(
                f'request_{username}',
                {
                    'type':'chat.message',
                    'status':True,
                    'data':data
                }
            )

    @database_sync_to_async
    def get_username(self, id):
        member = Member.objects.get(id=id)
        username = member.user.username
        print('username', username)
        return username
    
    @database_sync_to_async
    def request_exist(self, id):
        return Request.objects.filter(id=id).exists()

    async def chat_message(self, event):
        await self.send(
            json.dumps(event['data'])
        )
    