import sys
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async
#import asyncio
import json


def eprint(*args):
    print(*args, file=sys.stderr)

class UserConsumerError(Exception):
    pass
class UserConsumerWarning(Warning):
    pass

class UserConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.sockID = self.scope['url_route']['kwargs']['sock_id']

        if 'user' in self.scope:
            print('scope DOES contain user. ')
            self.user = self.scope['user']
            self.userID = self.user.id
            print(self.user)
            print('user id : ', self.user.id)
        else:
            raise UserConsumerError('A user tried to connect to a websocket without being logged in.')
        await self.accept()
        await self.send(text_data=json.dumps({
            'ev': 'connect',
            'msg': 'Hello there buddy !'
        }))


    async def disconnect(self, event):
        session_data = self.scope['session']
        try:
            session_data.pop("user_id")
            session_data.pop("user_login")
        except KeyError:
            eprint('Disconnecting AnonymousUser')
            raise StopConsumer

        eprint('UserConsumer :: disconnecting and wiping sessions data')
        session_data.delete()
        session_data.save()
        eprint('UserConsumer :: closing user websocket')
        self.user.is_active = False
        await sync_to_async(self.user.save)()
        raise StopConsumer