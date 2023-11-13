from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import json
import time

class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("REACHED GameConsumer.connect method !")
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f"game_{self.game_id}"
        
        if 'user' in self.scope:
            print('scope DOES contain user. ')
            user = self.scope['user']
            print(user)
            print('user id : ', user.id)
            
        else:
            print('scope DOES NOT contains user.')

        #user = self.scope['user']
        #username = None
        #if user.is_anonymous:   username = 'Anonymous'
        #else:                   username = user.username

        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'init_message',
                'msg': "Mon chien a mangé ma socket... Woof !"
                #'username': username
            }
        )
    
    async def init_message(self, event):
        
        msg = event['msg']
        #username = event['username']
        print("WwowW !")

        t0 = time.monotonic()
        for i in range(5):
            await self.send(text_data=json.dumps({'msg': msg + f" {i}"}))
            await asyncio.sleep(0.5)

        t1 = time.monotonic()

        delta_t = t1 - t0
        print(f"delta time : {delta_t}, fps : {5.0 / delta_t}")

        await self.send(text_data=json.dumps({'msg': msg + f" The dog is full and refuses to eat any more sockets."}))
        

        
    async def disconnect(self, event):
        self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        event_payload = json.loads(text_data)
        event_type = event_payload["event_type"]
        details = event_payload["details"]

        print('received event_type : ', event_type)
        print('received details :  ', details)

        # Send message to room group
        #await self.channel_layer.group_send(
        #    self.room_group_name, {"type": "chat.message", "message": message}
        #)
