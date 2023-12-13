'''
    This WebsocketNetworkAdaptor class is a singleton that manages the bidirectional 
    throughput between the AsyncWebsocketConsumers and the singleton
    GameManager instance that manages the async gameloops for all games.
    It's methods should be called when connecting and disconnecting clients 
    of websockets, and receiving and sending messages through them. 

    The standard format for sent and received messages from/to websockets is
    as follows : 

        - All messages start by an 'ev' field describing the event type of this
        specific communication. 
        
        List of event types received from the client: 
            1. 'start': Sets the client state as ready.
            2. 'stop': Player requests the game to stop.
                    This will stop the game (Opponent wins by default).
            3. 'keypress': Next to the 'ev' key will be a 'details' dict wih the dict key named 'key'
                    describing the keyboard input that triggered the event as str. 
                    To get its value, the event should be indexed as such : keypressed = event['details']['key']
            4. 'keyrelease' (ignorable): Same as format as 'keypress'.
            ...

        List of event types sent to the client:
            1. 'up': Event type for regular updates of game states. 
                    Next to the 'ev' dict key will be the 'state' key with the current game state as value.
                    See GameManager for details.
            2. 'disconnect' (Theoretical): Kicks out player from game, stops game for all players and cancel game records keeping.

        
'''

#COLLE

from abc import ABC
import json

from channels.layers import get_channel_layer

from users.models import User
from queue import Queue
import asyncio
import time
# from functools import wraps
from NetworkGateway.consumers import GameConsumer
from NetworkGateway.models import GameEvent
from game.models import Game
import game.PingPongRebound.defs as df
from asgiref.sync import sync_to_async, async_to_sync





# def async_to_sync_locked_class(func):
#     @wraps(func)
#     def __async_to_sync_game_locked(cls, *args, **kwargs):
#         async def __game_locked_exec(args, kwargs):
#             async with cls.__gateway_lock:
#                 func(cls, *args, **kwargs)
#         asyncio.run(__game_locked_exec(args, kwargs))
#     return __async_to_sync_game_locked


# def async_to_sync_locked(func):
#     @wraps(func)
#     def __async_to_sync_game_locked(self, *args, **kwargs):
#         async def __game_locked_exec(args, kwargs):
#             async with self.__gateway_lock:
#                 func(self, *args, **kwargs)
#         asyncio.run(__game_locked_exec(args, kwargs))
#     return __async_to_sync_game_locked

### Connector Clases
class BaseGateway(ABC):
    pass



class GameConnector:
    ''' Game connector holds the information necessary to handle the sending 
        of game updates.
    '''
    __channel_layer = get_channel_layer()
    __game_gateway = None # Set once by singleton GameGateway

    @classmethod
    def set_game_gateway(cls, game_gateway):
        if not cls.__game_gateway:
            cls.__game_gateway = game_gateway

    def __init__(self, sockID):
        self.__sockID = sockID
        self.__gameDB: Game = None# Database inst returned when creating game instance in database.
        self.__player_consumers: dict[int, GameConsumer] = dict()
        self.__game_lock = asyncio.Lock()
        self.__events_lock = asyncio.Lock()

        self.lobby_game = None # Returned after connecting to MatchMaker

        self.__events = asyncio.Queue()


    @property
    def is_running(self):
        return self.__gameID > 0
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
    
    def set_lobby_game(self, lgame):
        if self.lobby_game and lgame != self.lobby_game:
            GameGatwayException('Trying to set game_connector.lobby_game to different game. lobby_game can only be set once.')
        self.lobby_game = lgame
    
    def set_game_db_instance(self, game: Game):
        if not (game and isinstance(game, Game)):
            raise TypeError('Trying to set game instance to game connector, but object passed is not a Game model type.')
        self.__gameDB = game


    async def events(self):
        async with self.__events_lock:
            while not self.__events.empty():
                yield self.__events.get()
        #yield None

    async def getEvent(self):
        ev = None
        async with self.__events_lock:
            if not self.__events.empty():
                ev = self.__events.get()
        return ev

    async def getEvents(self):

        async with self.__events_lock:
            return [await self.__events.get() for _ in range(self.__events.qsize())]

    async def push_event(self, playerID, evType, key=None):
        event = GameEvent(playerID, evType, key)
        print("push_event: ", event)
        async with self.__events_lock:
            await self.__events.put(event)
            print('event queue length : ', self.__events.qsize())

    async def _send_players_list(self):
        async with self.__game_lock:
            names = self.lobby_game.player_names
        #payload = json.dumps(names)
        await self.__channel_layer.group_send(
            self.__sockID,
            {
                'type': 'game_new_connection_message',
                'players': names #payload
            }
        )

    async def connect_player(self, user, consumer):
        async with self.__game_lock:
            if user.id in self.__player_consumers:
                raise ValueError('Trying to add player to same game connector twice.')
            self.__player_consumers[user.id] = consumer

        await self.__channel_layer.group_add(
            self.__sockID,
            consumer.channel_name
        )
        asyncio.gather(
            self._send_players_list(),
        )


    async def disconnect_player(self, user):
        ''' Used to kickout player forcefully '''
        #if not self.gameID:
        #    raise GameGatwayException('GameConnector.disconnect_player() can only be called once the game is started. Otherwise call GameGateway.disconnect_player().')
        if not self.lobby_game:
            return None
        async with self.__game_lock:
            if user.id not in self.__player_consumers:
                raise ValueError(f"Trying to disconnect user {user.login} from a game they don't belong to.")
            consumer = self.__player_consumers.pop(user.id)
        

        await self.__channel_layer.group_discard(self.__sockID, consumer.channel_name)
        if self.game:
            ## TODO: Disconnect player while in live game. 
            await self.push_event(user.id, 'end_game') # send disconnect event to Game instance in game manager. Same place as keypress events.
        elif self.nb_connected > 0:
            ## 
            await self._send_players_list()
        #else:
        #    lgame, lply = self.match_maker.remove_player(user)
            #lply = self.lobby_game.remove_user(user)
            #asyncio.async_to_sync(self.__channel_layer.group_discard)(self.__sockID, pcons.channel_name)

    async def __send_state_change(self, ev_type, ev_key, ev_value):
        payload = json.dumps({
            'ev': ev_type,
            ev_key: ev_value
        })
        await self.__channel_layer.group_send(self.__sockID,
                {
                    'type': 'game_send_state',
                    'game_state': payload
                }
            )

    async def send_init_state(self, state):
        if not state:
            raise TypeError('No state was provided.')
        self.__send_state_change('init_game', 'init_state', state)

    async def send_end_state(self, state):
        if not state:
            raise TypeError('No state was provided.')
        self.__send_state_change('end_game', 'end_state', state)

    async def send_start_signal(self):
        print('<<< SENDING START SIGNAL !! >>>')
        payload = json.dumps({
            'ev': 'start'
        })
        await self.__channel_layer.group_send(self.__sockID,
                {
                    'type': 'game_send_state',
                    'game_state': payload
                }
            )
        # self.__send_state_change('start', 'start', '')
        
    async def send_score(self, scores):
        if not scores:
            raise TypeError('No scores was provided.')
        self.__send_state_change('scores', 'scores', scores)
        

    async def start_countdown(self):
        if not self.is_running:
            raise ValueError('Trying to start countdown, but game is not initialized.')
        
        event = {
            'ev': 'countdown',
            'counter': 3
        }

        for i in range(3):
            t_start = time.monotonic()
            payload = json.dumps(event)
            await self.__channel_layer.group_send(self.__sockID,
                {
                    'type': 'game.send.state',
                    'payload': payload
                }
            )
            payload['counter'] -= 1
            dt = time.monotonic() - t_start
            await asyncio.sleep(1.0 - dt)

        self.push_event(self.__sockID, 'start_game')





class GameGatwayException(Exception):
    pass

class GameGateway(BaseGateway):
    ''' Singleton object which orchestrats the sending of updates to all games '''

    def __init__(self):
        GameConnector.set_game_gateway(self)
        self.__channel_layer = get_channel_layer()
        self.__match_maker = None# Must be setup with self.set_matchmaker() before accepting connections
        self.__game_manager = None# Must be setup with self.set_gamemanager() before accepting connections

        #self.__connected_games: dict[str, GameConnector] = dict()
        self.__gateway_lock = asyncio.Lock()
        
    @property
    def match_maker(self):
        return self.__match_maker

    ### In setup phase, in GameConfig.ready()
    def set_match_maker(self, match_maker):
        if self.__match_maker:
            raise ValueError('Can only be setup once')
        self.__match_maker = match_maker

    def set_game_manager(self, game_manager):
        if self.__game_manager:
            raise ValueError('Can only be setup once')
        self.__game_manager = game_manager
    ########################################

    # async def contains_game(self, sockID):
        # res = False
        # async with self.__gateway_lock:
            # res = sockID in self.__connected_games
        # return res

    # async def __get_game_connector(self, sockID):
    #     gconn = None
    #     async with self.__gateway_lock:
    #         gconn = self.__connected_games.get(sockID)
    #     if gconn:
    #         return gconn
    #     else:
    #         return GameConnector(sockID)


    async def connect_player(self, sockID, consumer):
        ''' Called by websocket consumer connect() method. '''
        if not (self.__game_manager or self.__match_maker):
            raise ValueError('MatchMaker and GameManager must be set before accepting connections.')
        
        #gconn = await self.__get_game_connector(sockID)
        #await gconn.add_player(consumer.user, consumer)

        async with self.__gateway_lock:
            lobby_game = self.__match_maker.connect_player(consumer.user)
        if not lobby_game:
            raise GameGatwayException(f'User {consumer.user} connection to game FAILED !')

        #gconn.lobby_game = await self.__match_maker.connect_player(consumer.user)
        if not lobby_game.game_connector:
            gconn = GameConnector(sockID)
            lobby_game.set_game_connector(gconn)
            gconn.set_lobby_game(lobby_game)
        else:
            gconn = lobby_game.game_connector

        await gconn.connect_player(consumer.user, consumer)
        await gconn.send_init_state(self.__game_manager.getInitInfo(lobby_game.gameType))


        # if gconn.lobby_game:
        #     print('Connected to game with SUCCESS ! LobbyGame : ', gconn.lobby_game)
        #     print('Connected Lobby game : ', gconn.lobby_game)
        #     #print('is game ready ? ', self.__match_maker.is_game_ready(gconn.lobby_game))
        # else:
        #     #print(f'User {self.user} connection to game FAILED !')
        #     raise GameGatwayException(f'User {consumer.user} connection to game FAILED !')

        # async with self.__gateway_lock:
        #     self.__connected_games[sockID] = gconn

        # await self.__channel_layer.group_send(
        #     lobby_game.sockID,
        #     {
        #         'type': 'game_new_connection_message',
        #         'players': json.dumps(lobby_game.player_names)
        #         #'username': username
        #     }
        # )
        return gconn
    

    async def disconnect_player(self, user: User):
        ''' This method should only be used to disconnect players while in lobby. '''
        async with self.__gateway_lock:
            rem = self.match_maker.remove_player(user)
        if not rem:
            raise GameGatwayException(f"Trying to disconnect user {user.login} from lobby, but was not found there.")
        lgame, lply = rem
        if not lgame.is_empty:
            lgame.game_connector.disconnect_player(user)
            #lgame.game_connector._send_players_list()


    @sync_to_async
    def __create_db_game(self, lgame, gameType, maxPlayers):#, **kwargs):
        game = Game.objects.create(
            game_type=gameType,
            max_players=maxPlayers#self._maxRacketCounts[gameType]
        )
        for lply in lgame.players:
            game.add_player(lply.user, save=False)
        game.declare_started(save=True)
        lgame.game_connector.set_game_db_instance(game)
        return game

    async def __push_game_to_gamemanager(self, gameType: str, lgame):
        ''' When calling this function, the game should be validated ready to start. '''
        #game = await self.__create_db_game(lgame, gameType, self.__game_manager.getMaxPlayerCount[gameType])
        print('lgame type : ', type(lgame))
        print('gameType type : ', type(gameType))

        # Checks if is local game with 2 local players on same keyboard or single player on board. Passes the result to addGame().
        GameManagerMode = df.DUAL if (lgame.gameMode == 'Local_2p') else df.SOLO
        
        game = await self.__create_db_game(lgame, gameType, self.__game_manager.getMaxPlayerCount(gameType))

        self.match_maker.remove_lobby_game(lgame)
        game_connector = lgame.game_connector
        gm = self.__game_manager

        print('game after sync_to_async db game creation : ', game)
        gm_status = await gm.addGame(
            gameType,
            lgame.sockID,
            connector=game_connector,
            gameMode=GameManagerMode
        )
        if not gm_status:
            raise GameGatwayException('Error occured while trying to create new game in game_manager.')

        tasks = [gm.addPlayerToGame(lply.user.id, lply.user.login, lgame.sockID) for lply in lgame.players]
        await asyncio.gather(*tasks)
        # await game_connector.send_init_state(gm.getInitInfo(gameType))
        
        await lgame.game_connector.send_start_signal()
        await gm.startGame(lgame.sockID)
        #lgame.set_is_started()
        return lgame


    async def set_player_ready(self, user: User):
        ''' Called from a sync HTTP POST request, so no reference to lobby_game
        or game_connector unlike websocket messages with consumer. '''
        async with self.__gateway_lock:
            lgame = self.match_maker.set_ready(user)

        if not lgame:
            raise GameGatwayException(f"Trying to set user {user.login} as ready, but wasn't found in lobby.")

        print(f"Trying to set user {user.id} as ready")
        if lgame.is_ready:
            ## SEND GAME TO GAME MANAGER
            print('\n\n GAME IS READY !!! ')
            print('SENDING GAME TO MANAGER !!! ')
            await self.__push_game_to_gamemanager(lgame.gameType, lgame)
            print(f"Lobby Game send to game manager : ", {lgame})
            


    async def __send_single_async_update(self, game_id, state, ev_wrap):
        if not state:
            raise ValueError('Trying to send empty state to client.')
        # print('sending game state to socket : ', game_id)
        if ev_wrap:
            state = {
                'ev': 'up',
                'state': state
            }

        payload = json.dumps(state)
        # await self.__channel_layer.group_send(game_id,
        await self.__channel_layer.group_send(game_id,
            {
                'type': 'game_send_state',
                'game_state': payload
            }
        )


    async def async_send_all_updates(self, game_states: dict[str, any], ev_wrap=False):
        # tasks = []
        for game_id, state in game_states.items():
            # tasks.append(self.__send_single_async_update(game_id, state, ev_wrap))
            await self.__send_single_async_update(game_id, state, ev_wrap)
 


    async def manage_end_game(end_game_state: dict):
        ''' Will deal with either individual games or tournament games. Called by GameManager at the end of a game. '''
        pass

