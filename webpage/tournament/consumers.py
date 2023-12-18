import sys
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async
from tournament.models import Tournament
from game.apps import GameConfig as app
# from game.MatchMaker import LobbyGame
from NetworkGateway.consumers import GameConsumer
import asyncio
import json

def eprint(*args):
    print(*args, file=sys.stderr)



class TournamentConnector:
    ''' Tournament connector holds the information necessary to handle the sending
        of Tournament updates.
    '''
    __channel_layer = get_channel_layer()
    __game_gateway = None # Set once by singleton GameGateway

    @classmethod
    def set_game_gateway(cls, game_gateway):
        if not cls.__game_gateway:
            cls.__game_gateway = game_gateway

    def __init__(self, initLobby):
        # self.__sockID: str = sockID
        self.__tourDB: Tournament = None# Database instance returned when creating game instance in database.
        self.__player_consumers: dict[int, GameConsumer] = dict()
        self.__initLobby = initLobby
        self.__tour_lock = asyncio.Lock()
        print('Creating TournamentConnector :: with sockID : ', self.sockID)

        # self.__tournament = 
        # self.lobby_game = None # Returned after connecting to MatchMaker


    @property
    def is_running(self):
        return self.__tourID > 0
    @property
    def nb_connected(self):
        return len(self.__player_consumers)
    #@property
    #def match_maker(self):
    #    return self.__game_gateway.match_maker
    @property
    def tournament(self):
        return self.__tourDB
    # @property
    # def tourID(self):
    #     return self.__tourDB.id
    @property
    def sockID(self):
        return self.__initLobby.tourID
        # return self.__sockID

   # def set_lobby_game(self, lgame):
   #     if self.lobby_game and lgame != self.lobby_game:
   #         GameGatwayException('Trying to set game_connector.lobby_game to different game. lobby_game can only be set once.')
   #     self.lobby_game = lgame

    def set_tour_db_instance(self, tour: Tournament):
        if not (tour and isinstance(tour, Tournament)):
            raise TypeError('Trying to set tour instance to TournamentConnector, but object passed is not a Tournament model type.')
        self.__tourDB = tour


    async def connect_player(self, user, consumer):
        async with self.__tour_lock:
            if user.id in self.__player_consumers:
                raise ValueError('Trying to add player to same game connector twice.')
            self.__player_consumers[user.id] = consumer

        await self.__channel_layer.group_add(
            self.sockID,
            consumer.channel_name
        )
        # asyncio.gather(
        # await self.send_brackets()
        # )


    async def disconnect_player(self, user):
        print(f'GameConnector :: ENTER disconnect player')
        if not self.lobby_game:
            return None
        async with self.__game_lock:
            if user.id not in self.__player_consumers:
                raise ValueError(f"Trying to disconnect user {user.login} from a game they don't belong to.")
            consumer = self.__player_consumers.pop(user.id)

        #await self.send_end_state(end_state);

        await self.__channel_layer.group_discard(self.sockID, consumer.channel_name)

        print(f'GameConnector :: SWITCH')
        if self.game:
            ## TODO: Disconnect player while in live game.
            print(f'GameConnector :: disconnect player {user.id} INGAME')
            await self.push_event(user.id, 'end_game') # send disconnect event to Game instance in game manager. Same place as keypress events.
        elif self.nb_connected > 0:
            ##
            print(f'GameConnector :: disconnect player {user.id} while IN LOBBY')
            await self._send_players_list()
        else:
            print('WTF DUDE !!')


    async def send_brackets(self, brackets_info):

        payload = json.dumps({
            'ev': 'brackets',
            'info': brackets_info
        })
        await self.__channel_layer.group_send(
            self.sockID,
            {
                'type': 'tour_new_connection_message',
                'brackets': payload
            }
        )


    # async def _send_players_list(self):
    #     async with self.__game_lock:
    #         players = self.lobby_game.players

    #     # payload = json.dumps([
    #     payload = [
    #         {
    #             'login': ply.user.login,
    #             'img': ply.user.img_link,
    #             'ready': ply.is_ready
    #         }
    #         for ply in players
    #     ]
    #     print('send player info payload : ', payload)

    #     #payload = json.dumps(names)
    #     await self.__channel_layer.group_send(
    #         self.__sockID,
    #         {
    #             'type': 'game_new_connection_message',
    #             'players': payload
    #         }
    #     )


    # async def __send_state_change(self, ev_type, ev_key, ev_value):
    #     payload = json.dumps({
    #         'ev': ev_type,
    #         ev_key: ev_value
    #     })
    #     await self.__channel_layer.group_send(self.__sockID,
    #             {
    #                 'type': 'game_send_state',
    #                 'game_state': payload
    #             }
    #         )

    # async def send_init_state(self, state):
    #     if not state:
    #         raise TypeError('send_init_state :: No state was provided.')
    #     self.__send_state_change('init_game', 'init_state', state)

    # async def send_end_state(self, state):
    #     if not state:
    #         raise TypeError('send_end_state :: No state was provided.')
    #     print('CALLED send_end_state()')
    #     # self.__send_state_change('end', 'end_state', state)


    #     payload = json.dumps({
    #         'ev': 'end',
    #         'end_state': state
    #     })
    #     await self.__channel_layer.group_send(self.__sockID,
    #             {
    #                 'type': 'game_send_end_state',
    #                 'end_state': payload
    #             }
    #         )

    # async def send_start_signal(self):
    #     print('<<< SENDING START SIGNAL !! >>>')
    #     payload = json.dumps({
    #         'ev': 'start'
    #     })
    #     await self.__channel_layer.group_send(self.__sockID,
    #             {
    #                 'type': 'game_send_state',
    #                 'game_state': payload
    #             }
    #         )
    #     # self.__send_state_change('start', 'start', '')

    # async def send_score(self, scores):
    #     if not scores:
    #         raise TypeError('No scores was provided.')
    #     self.__send_state_change('scores', 'scores', scores)



class TournamentConsumerError(Exception):
    pass
class TournamentConsumerWarning(Warning):
    pass

class TournamentConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.sockID = self.scope['url_route']['kwargs']['sock_id']
        print('tournament :::::: CONNECTING TO WEBSOCKET with id : ', self.sockID)

        self.netGateway = app.get_game_gateway()
        if 'user' in self.scope:
            print('scope DOES contain user. ')
            self.user = self.scope['user']
            self.userID = self.user.id
            print(self.user)
            print('user id : ', self.user.id)
        else:
            raise TournamentConsumerError('A tournament tried to connect to a websocket without being logged in.')
        
        await self.accept()

        await self.netGateway.connect_to_tournament(self.user, self)

        await self.send(text_data=json.dumps({
            'ev': 'connect',
            'msg': 'Hello there buddy !'
        }))


    async def disconnect(self, event):
        # session_data = self.scope['session']
        # session_data.pop("tournament_id")
        # session_data.pop("tournament_login")
        # session_data.save()
        print('\n\ntournament Websocket disconnecting !\n\n')
        eprint('TournamentConsumer :: disconnecting and wipping sessions data')
        # session_data.delete()
        # #Save deletes the session data and the session key, and it deletes the session from the database.
        # session_data.save()
        eprint('TournamentConsumer :: closing tournament websocket')
        self.tournament.is_active = False
        await sync_to_async(self.tournament.save)()
        raise StopConsumer

    async def tour_new_connection_message(self, event):
        await self.send(text_data=event['brackets'])