from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
#import asyncio
import json
import time

from game.apps import GameConfig as app


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
        print('From cunsumer try connect player')
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
        await self.netGateway.set_player_ready(self.user)


    async def disconnect(self, event):
        ### REWORK NEEDED
        print('Websocket disconnecting !')
        if self.game_connector.lobby_game:
            self.game_connector.disconnect_player(self.user)
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
        
        # await self.game_connector.push_event(event)
        await self.game_connector.push_event(self.userID, event_type, key)


    async def game_new_connection_message(self, event):

        payload = {
            'ev': 'connection',
            'player_list': event['players']#self.lobby_game.player_names#[lply.user.display_name for lply in self.lobby_game.players]
        }
        await self.send(text_data=json.dumps(payload))

    
    async def game_send_state(self, event):
        ''' specifically for sending game state updates '''
        print('game_send_state was here !')
        await self.send(text_data=event['game_state'])

    async def game_send_event(self, event):
        ''' For sending all other game events to player. payload should 
        be network ready.'''
        await self.send(text_data=event['payload'])
        



"""
class GameConsumer(AsyncWebsocketConsumer):
    
    #public_games = dict()
    #tournament_games = dict()# structured tournament_games[<tournament_name>][<game_id>]

    # async def validate_user_can_connect_to_game(self, user):
    #    '''
    #        Validates that : 
    #            - User is not already connected to a game.
    #            - The game isn't already full.
    #    '''

    #    if user.running_game:
    #        if user.running_game in self.public_games:
    #            # User trying to reconnect to the game they are already connected to.
    #            return False
           
    #        if self.public_games[user.running_game]:
    #            pass




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
            print('scope DOES NOT contain user.')

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
            await asyncio.sleep(1)

        t1 = time.monotonic()

        delta_t = t1 - t0
        print(f"delta time : {delta_t}, fps : {5.0 / delta_t}")

        await self.send(text_data=json.dumps({'msg': msg + f" The dog is full and refuses to eat any more sockets."}))
        

        
    async def disconnect(self, event):
        self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )
        raise StopConsumer


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
        #if event_type == 'test':

        ### Currently just a ping response
        await self.send(text_data=json.dumps({'msg': 'async message received. wow.', 'event_type': event_type, 'details': details}))
        

    async def game_send_data(self, event):
        await self.send(text_data=event['game_state'])
"""