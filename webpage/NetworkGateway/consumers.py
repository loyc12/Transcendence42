import sys
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
#import asyncio
import json
import time

from game.apps import GameConfig as app

def eprint(*args):
    print(*args, file=sys.stderr)

class GameConsumerError(Exception):
    pass
class GameConsumerWarning(Warning):
    pass

class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.sockID = self.scope['url_route']['kwargs']['sock_id']
        self.game_connector = None # While be set by GameGateway

        if 'user' in self.scope:
            self.user = self.scope['user']
            self.userID = self.user.id

        else:
            raise GameConsumerError('A user tried to connect to a websocket without being logged in.')
        
        self.netGateway = app.get_game_gateway()
        await self.accept()
        self.game_connector = await self.netGateway.connect_player(self.sockID, self)



    async def disconnect(self, event):
        eprint(f'GameConsumer disconnecting ! user : ', self.user.login)
        await self.netGateway.disconnect_player(self.user, self)
        eprint(f'GameConsumer finished disconnecting !')
        raise StopConsumer


    @staticmethod
    def __validate_receive_msg(event: dict):
        return 'ev' in event

    async def receive(self, text_data):
        event = json.loads(text_data)
        if not self.__validate_receive_msg(event):
            raise GameConsumerWarning('Reveived message is malformed.')

        # Clean up input struct.
        event_type = event['ev']
        key = event['key'] if 'key' in event else None

        if event_type == 'ready':
            await self.netGateway.set_player_ready(self.user)
        else:
            await self.game_connector.push_event(self.userID, event_type, key)



    async def game_new_connection_message(self, event):

        payload = {
            'ev': 'connection',
            'player_list': event['players'] #self.lobby_game.player_names#[lply.user.display_name for lply in self.lobby_game.players]
        }
        await self.send(text_data=json.dumps(payload))


    async def game_send_state(self, event):
        ''' specifically for sending game state updates '''
        await self.send(text_data=event['game_state'])

    async def game_send_event(self, event):
        ''' For sending all other game events to player. payload should
        be network ready.'''
        await self.send(text_data=event['payload'])

    async def game_send_state(self, event):
        ''' specifically for sending game state updates '''
        await self.send(text_data=event['game_state'])

    async def game_send_end_state(self, event):
        ''' specifically for sending game state updates '''
        await self.send(text_data=event['end_state'])

