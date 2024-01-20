from channels.layers import get_channel_layer
import asyncio
import json
from queue import Queue
import time
from NetworkGateway.consumers import GameConsumer
from NetworkGateway.models import GameEvent
from game.models import Game

class GameConnectorError(Exception):
    pass


class GameConnector:
    __channel_layer = get_channel_layer()
    __game_gateway = None # Set once by singleton GameGateway

    #  DEFINE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @classmethod
    def set_game_gateway(cls, game_gateway):
        if not cls.__game_gateway:
            cls.__game_gateway = game_gateway

    def __init__(self, sockID):
        self.__sockID = sockID
        self.__gameDB: Game = None# Database instance returned when creating game instance in database.
        self.__player_consumers: dict[int, GameConsumer] = dict()
        self.__game_lock = asyncio.Lock()
        self.__events_lock = asyncio.Lock()
        self.__lobby_game = None # Returned after connecting to MatchMaker
        self.__events = asyncio.Queue()
        self.__scores: list = []
        self.__is_closing = False

    def __contains__(self, user):
        return user.id in self.__player_consumers

    @property
    def is_running(self):
        return self.__gameDB is not None
    @property
    def nb_connected(self):
        return len(self.__player_consumers)
    @property
    def match_maker(self):
        return self.__game_gateway.match_maker
    @property
    def game(self):
        return self.__gameDB
    @property
    def gameID(self):
        return self.__gameDB.id
    @property
    def lobby_game(self):
        return self.__lobby_game
    @property
    def is_tournament_game(self):
        return self.__lobby_game.is_tournament_game


    #  SETTER  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def set_lobby_game(self, lgame):
        if self.__lobby_game and lgame != self.__lobby_game:
            GameConnectorError('Trying to set game_connector.__lobby_game to different game. lobby_game can only be set once.')
        self.__lobby_game = lgame
    def set_game_db_instance(self, game: Game):
        if not (game and isinstance(game, Game)):
            raise TypeError('Trying to set game instance to game connector, but object passed is not a Game model type.')
        self.__gameDB = game

    #  SETTER  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Get all events one by one
    async def events(self):
        async with self.__events_lock:
            while not self.__events.empty():
                yield self.__events.get()
    #  Get all events as a list
    async def getEvents(self):
        async with self.__events_lock:
            return [await self.__events.get() for _ in range(self.__events.qsize())]
    #  Get one event (ev)
    async def getEvent(self):
        ev = None
        async with self.__events_lock:
            if not self.__events.empty():
                ev = self.__events.get()
        return ev
    async def update_scores(self, scores):
        self.__scores = scores

   #  PUSH_EVENT  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    async def push_event(self, playerID, evType, key=None):
        event = GameEvent(playerID, evType, key)
        async with self.__events_lock:
            await self.__events.put(event)

   #  STATE_EVENT  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   # INIT_STATE
    async def send_init_state(self, state):
        if not state:
            raise TypeError('send_init_state :: No state was provided.')
        self.__send_state_change('init_game', 'init_state', state)
    # STATE_CHANGE
    async def __send_state_change(self, ev_type, ev_key, ev_value):
        payload = json.dumps({ 'ev': ev_type, ev_key: ev_value })
        await self.__channel_layer.group_send(self.__sockID,
                {
                    'type': 'game_send_state',
                    'game_state': payload
                }
            )
    # END_STATE
    async def send_end_state(self, state):
        if not state:
            raise TypeError('send_end_state :: No state was provided.')
        payload = json.dumps({ 'ev': 'end', 'end_state': state })
        await self.__channel_layer.group_send(self.__sockID,
                {
                    'type': 'game_send_end_state',
                    'end_state': payload
                }
            )
    # CONNECTION//DECONNECTION EVENT  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # CONNECTION
    async def connect_player(self, user, consumer):
        async with self.__game_lock:
            if user.id in self.__player_consumers:
                raise ValueError('Trying to add player to same game connector twice.')
            self.__player_consumers[user.id] = consumer
        await self.__channel_layer.group_add(
            self.__sockID,
            consumer.channel_name
        )
        await self._send_players_list()


    # DECONNECTION
    async def disconnect_player(self, user, quitter=None):
        if not self.__lobby_game or user.id not in self.__player_consumers:
            return None
        async with self.__game_lock:
            if user.id not in self.__player_consumers:
                raise ValueError(f"Trying to disconnect user {user.login} from a game they don't belong to.")
            consumer = self.__player_consumers.pop(user.id)

        if quitter is None:
            await self.__channel_layer.group_discard(self.__sockID, consumer.channel_name)
        if self.game and self.game.is_running:
            if self.__is_closing:
                return
             # send disconnect event to Game instance in game manager. Same place as keypress events.

            self.__is_closing = True
            if quitter is None:
                await self.push_event(user.id, 'end_game')
            else:
                await self.push_event(quitter, 'end_game')

        elif self.nb_connected > 0:
            ''' Player disconnects in game lobby '''
            # send updated player list to all players without the disconnected player
            await self._send_players_list()

        elif self.__lobby_game.is_tournament:
            print(f'GameConnector :: disconnect player {user.id} from tournament lobby.')

        else:
            print('WTF DUDE !! async def disconnect_player(self, user), other')


    async def disconnect_all_players(self, quitter=None):
        player_list = list(self.__player_consumers.keys())
        for playerID in player_list:
            if playerID in self.__player_consumers:
                await self.disconnect_player(self.__player_consumers[playerID].user, quitter)

    async def find_user_with_api_key(self, userApiKey):
        async with self.__game_lock:
            for cons in self.__player_consumers.values():
                if cons.user.apiKey == userApiKey:
                    return cons.user
        return None


    # INFORMATION SENDING EVENT  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Get all players as a list
    async def _send_players_list(self):
        async with self.__game_lock:
            # Players list from lobby_game
            players = self.__lobby_game.players
        # Payload to send to all players
        payload = [ { 'login': ply.user.login, 'img': ply.user.img_link, 'ready': ply.is_ready }
            for ply in players ]
        await self.__channel_layer.group_send(
            self.__sockID,
            {
                'type': 'game_new_connection_message',
                'players': payload
            }
        )
    # Send start signal to SOCKID
    async def send_start_signal(self):
        payload = json.dumps({ 'ev': 'start' })
        await self.__channel_layer.group_send(self.__sockID,
                {
                    'type': 'game_send_state',
                    'game_state': payload
                }
            )
    # Send score
    async def send_score(self, scores):
        if not scores:
            raise TypeError('No scores was provided.')
        self.__send_state_change('scores', 'scores', scores)
