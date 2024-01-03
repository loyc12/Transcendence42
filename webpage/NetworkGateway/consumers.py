import sys
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
#import asyncio
import json
import time

from game.apps import GameConfig as app



def eprint(*args):
    print(*args, file=sys.stderr)

# class IDConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

# # - - - - - - -  -

class GameConsumerError(Exception):
    pass
class GameConsumerWarning(Warning):
    pass

class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.sockID = self.scope['url_route']['kwargs']['sock_id']
        print('CONNECTING TO WEBSOCKET with id : ', self.sockID)
        self.game_connector = None # While be set by GameGateway

        if 'user' in self.scope:
            print('scope DOES contain user. ')
            self.user = self.scope['user']
            self.userID = self.user.id
            print(self.user)
            print('user id : ', self.user.id)
        else:
            raise GameConsumerError('A user tried to connect to a websocket without being logged in.')

        # await self.channel_layer.group_add(
        #     self.sockID,
        #     self.channel_name
        # )
        #self.match_maker = app.get_match_maker()
        self.netGateway = app.get_game_gateway()
        print('From consumer try connect player')
        # self.lobby_game = await self.match_maker.connect_player(self.user)
        # if self.lobby_game:
        #     print('Connected to game with SUCCESS ! LobbyGame : ', self.lobby_game)
        #     print('Connected Lobby game : ', self.lobby_game)
        #     print('is game ready ? ', self.match_maker.is_game_ready(self.lobby_game))
        # else:
        #     #print(f'User {self.user} connection to game FAILED !')
        #     raise GameConsumerError(f'User {self.user} connection to game FAILED !')

        await self.accept()

        self.game_connector = await self.netGateway.connect_player(self.sockID, self)

        ### DEBUG ONLY
        #await self.netGateway.set_player_ready(self.user)


    async def disconnect(self, event):
        ### REWORK NEEDED
        eprint(f'GameConsumer disconnecting ! user : ', self.user.login)
        await self.netGateway.disconnect_player(self.user, self)
        eprint(f'GameConsumer finished disconnecting !')
            # self.game_connector.disconnect_player(self.user)
            #if self.game_connector.game:
            #else:
            #    self.netGateway.diconnect_player(self.user)
        #...
        #self.match_maker.remove_player(self.user)
        #self.match_maker.gm.
        #self.netGateway.remove_player(self.user)
        #self.lobby_game = None
        #...
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
            print('\n\n GAME READY SIGNAL RECEIVED SERVERSIDE !!')
            await self.netGateway.set_player_ready(self.user)
        else:
            # await self.game_connector.push_event(event)
            await self.game_connector.push_event(self.userID, event_type, key)



    async def game_new_connection_message(self, event):

        payload = {
            'ev': 'connection',
            'player_list': event['players'] #self.lobby_game.player_names#[lply.user.display_name for lply in self.lobby_game.players]
        }
        print('payload ready to go ! ', payload)
        await self.send(text_data=json.dumps(payload))


    async def game_send_state(self, event):
        ''' specifically for sending game state updates '''
        # print('game_send_state was here !')
        await self.send(text_data=event['game_state'])

    async def game_send_event(self, event):
        ''' For sending all other game events to player. payload should
        be network ready.'''
        await self.send(text_data=event['payload'])

    async def game_send_state(self, event):
        ''' specifically for sending game state updates '''
        # print('game_send_state was here !')
        await self.send(text_data=event['game_state'])

    async def game_send_end_state(self, event):
        ''' specifically for sending game state updates '''
        # print('game_send_state was here !')
        await self.send(text_data=event['end_state'])

