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
        print('USER :::::: CONNECTING TO WEBSOCKET with id : ', self.sockID)

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
        ### DELETE
        print('\n\nUser Websocket disconnecting !\n\n')
        # await self.netGateway.disconnect_player(self.user, self)
        #logout(self.user)
        session_data = self.scope['session']
        #Flush does not delete the session, it just removes the session data while keeping the session key.
        #session_data.flush()
        #Clear deletes the session data and the session key.
        #session_data.clear()
        #Delete deletes the session data and the session key, but it doesn't delete the session from the database.
        eprint('UserConsumer :: disconnecting and wipping sessions data')
        session_data.delete()
        #Save deletes the session data and the session key, and it deletes the session from the database.
        session_data.save()
        eprint('UserConsumer :: closing user websocket')
        self.user.is_active = False
        await sync_to_async(self.user.save)()
        # await self.close()
        raise StopConsumer


    # @staticmethod
    # def __validate_receive_msg(event: dict):
    #     return 'ev' in event

    # async def receive(self, text_data):
    #     event = json.loads(text_data)
    #     if not self.__validate_receive_msg(event):
    #         raise UserConsumerWarning('Reveived message is malformed.')


    # async def User_new_connection_message(self, event):

    #     payload = {
    #         'ev': 'connection',
    #         'player_list': event['players'] #self.lobby_User.player_names#[lply.user.display_name for lply in self.lobby_User.players]
    #     }
    #     print('payload ready to go ! ', payload)
    #     await self.send(text_data=json.dumps(payload))


    # async def User_send_state(self, event):
    #     ''' specifically for sending User state updates '''
    #     # print('User_send_state was here !')
    #     await self.send(text_data=event['User_state'])
