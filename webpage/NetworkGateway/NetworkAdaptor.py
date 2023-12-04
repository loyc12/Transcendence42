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


from abc import ABC
import json

from channels.layers import get_channel_layer

from users.models import User
from queue import Queue
import asyncio
import time
from functools import wraps
from NetworkGateway.consumers import GameConsumer
from game.models import Game
from asgiref.sync import sync_to_async




def async_to_sync_locked_class(func):
    @wraps(func)
    def __async_to_sync_game_locked(cls, *args, **kwargs):
        async def __game_locked_exec(args, kwargs):
            async with cls.__gateway_lock:
                func(cls, *args, **kwargs)
        asyncio.run(__game_locked_exec(args, kwargs))
    return __async_to_sync_game_locked


def async_to_sync_locked(func):
    @wraps(func)
    def __async_to_sync_game_locked(self, *args, **kwargs):
        async def __game_locked_exec(args, kwargs):
            async with self.__gateway_lock:
                func(self, *args, **kwargs)
        asyncio.run(__game_locked_exec(args, kwargs))
    return __async_to_sync_game_locked

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
        
    async def get_event(self):
        ev = None
        async with self.__events_lock:
            if not self.__events.empty():
                ev = self.__events.get()
        return ev    

    async def push_event(self, event):
        async with self.__events_lock:
            self.__events.put(event)

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
        await self._send_players_list()

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
        
        #if self.game:
            ### TODO: Disconnect player while in live game. 
           # self.push_event({
           #     'ev': 'disconnect',
           #     'gameID': self.__sockID,
           #     'playerID': user.id
           # })
        if self.nb_connected > 0:
            await self._send_players_list()
        #else:
        #    lgame, lply = self.match_maker.remove_player(user)
            #lply = self.lobby_game.remove_user(user)
        await self.__channel_layer.group_discard(self.__sockID, consumer.channel_name)
            #asyncio.async_to_sync(self.__channel_layer.group_discard)(self.__sockID, pcons.channel_name)


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
            await self.__channel_layer.group_send(self.__game_id,
                {
                    'type': 'game.send.state',
                    'payload': payload
                }
            )
            payload['counter'] -= 1
            dt = time.monotonic() - t_start
            await asyncio.sleep(1.0 - dt)

        self.push_event({
            'ev': 'start'
        })





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
        #print('self.__game_manager.getMaxPlayerCount(gameType) type : ', type(self.__game_manager.getMaxPlayerCount(gameType)))
        game = await self.__create_db_game(lgame, gameType, self.__game_manager.getMaxPlayerCount(gameType))

        self.match_maker.remove_lobby_game(lgame)
        game_connector = lgame.game_connector
        gm = self.__game_manager
        print('game after sync_to_async db game creation : ', game)
        gm_status = await gm.addGame(gameType, lgame.sockID)
        if not gm_status:
            raise GameGatwayException('Error occured while trying to create new game in game_manager.')


        #tasks = [self.gm.addPlayerToGame(lply.user.id, lply.user.login, game.id) for lply in lgame.players]
        #await asyncio.gather(tasks)
        tasks = [gm.addPlayerToGame(lply.user.id, lply.user.login, lgame.sockID) for lply in lgame.players]
        #async for lply in lgame.players:
        #    tasks.append(gm.addPlayerToGame(lply.user.id, lply.user.login, game.id))
        await asyncio.gather(*tasks)
        await gm.startGame(lgame.sockID)
        #lgame.set_is_started()
        return lgame

    #async def __start_game(self, lgame):
    #    ''' Assumes lgame.is_ready == True '''
    #    await self.__game_manager.addGame(lgame.gameType, lgame.sockID)




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
            await self.__push_game_to_gamemanager(lgame.gameType, lgame)
            print(f"Lobby Game send to game manager : ", {lgame})


    '''
    @async_to_sync_locked
    def track_game(self, game_id, player_consumers):
        gconn = GameConnector(game_id, player_consumers)
        self.__channel_layer[game_id] = gconn

    @async_to_sync_locked
    def remove_game(self, game_id):
        if game_id in self.__connected_games:
            self.__connected_game.pop(game_id)
    '''

    async def async_send_all_updates(self, game_states: dict[str, any], ev_wrap=False):
        async for game_id, state in game_states:
            if not state:
                raise ValueError('Trying to send empty state to client.')
            #if not await self.contains_game(game_id):
            #    raise ValueError('Trying to send update to non-existant game_id.')
            if ev_wrap:
                state = {
                    'ev': 'up',
                    'state': state
                }

            payload = json.dumps(state)
            await self.__channel_layer.group_send(game_id,
                {
                    'type': 'game.send.state',
                    'game_state': payload
                }
            )
        
    
    #def send_all_updates(self, game_states: dict[int, any], ev_wrap=False):
    #    asyncio.run(self.send_all_updates(game_states, ev_wrap))


    





"""
class PlayerConnector(BaseGateway):

    def __init__(self, consumer: GameConsumer):#, position: int=1):
        self.consumer: GameConsumer = consumer
        #self.position: int = position

    async def send_disconnect_signal(self):
        payload = json.dumps({
            'ev': 'disconnect'
        })
        await self.consumer.send(text_data=payload)


    #async def send_current_state(self, state):
#
    #    if not state:
    #        raise ValueError('Trying to send empty state to client.')
    #    
    #    payload = json.dumps(state)
    #    await self.consumer.send(text_data=payload)
"""

"""
class GameGateway(BaseGateway):

    __channel_layer = None
    __all_connected_games = dict()
    __games_lock = asyncio.Lock()

    def __init__(self, game_id: str):
        if game_id in self.__all_connected_games():
            raise ValueError('GameGateway cannot create two gateways for the same game.')
        if not self.__channel_layer:
            self.__channel_layer = get_channel_layer()
        self.__game_id: str = game_id
        self.__connected_players: dict[int, PlayerConnector] = dict()
        self.__player_events = Queue()
        self.__events_lock = asyncio.Lock()

        self.__all_connected_games[game_id] = self
        self.__register_self_to_class(game_id, self)

    def __del__(self):
        self._deregister_self_from_class(self.game_id)


    #@classmethod
    #def __dec_get_lock(cls):
    #    return cls.__games_lock
    #@classmethod
    #def __async_to_sync_game_locked(cls, func, *args, **kwargs):
    #    async def __game_locked_exec(func, args, kwargs):
    #        async with cls.__games_lock:
    #            func(*args, **kwargs)
    #    asyncio.run(__game_locked_exec(func, args, kwargs))

    @async_to_sync_locked
    def contains_game(self, game_id):
        return game_id in self.__all_connected_games
    

    @async_to_sync_locked_class
    def _register_self_to_class(cls, game_id, self):
        cls.__all_connected_games[game_id] = self
        #def __locked_register(game_id, self):
        #    if game_id in cls.__all_connected_games:
        #        raise ValueError('Trying to add ')
        #    cls.__all_connected_games[game_id] = self
        #cls.__async_to_sync_game_locked(__locked_register, game_id, self)

#        async def __lock_register(cls, game_id, self):
#            async with cls.__games_lock:
#                if game_id in cls.__all_connected_games:
#                    raise ValueError('Trying to add ')
#                cls.__all_connected_games[game_id] = self
#        asyncio.run(__lock_register(cls, game_id, self))

    @async_to_sync_locked_class
    def _deregister_self_to_class(cls, game_id):
        if game_id in cls.__all_connected_games:
            cls.__all_connected_games.pop(game_id)

    #@classmethod
    #def __deregister_self_from_class(cls, game_id):
    #    def __locked_deregister(game_id, self):
    #        if (game_id in cls.__all_connected_games):
    #            cls.__all_connected_games.pop(game_id)
    #    cls.__async_to_sync_game_locked(__locked_deregister, game_id)

        #async def __lock_deregister(cls, game_id):
        #    async with cls.__games_lock:
        #        if (game_id in cls.__all_connected_games):
        #            cls.__all_connected_games.pop(game_id)
        #asyncio.run(__lock_deregister(game_id))

    @classmethod
    def send_all_game_updates(cls, game_states: dict[int, any]):
        '''
            Takes a dict of game states, provided by GameManager,
            with user id as key and a game state in json serializable dict format.
            See GameManager for more details about game state.
        '''
        # Starts the sending process for all groups ...
        tasks = []
#        tasks = [self.__all_connected_games[game_id].send_current_state(state, ev_wrap=False) for game_id, state in game_states if game_id in self.__all_connected_games]
        #asyncio.gather(*tasks, return_exceptions=True)
        for game_id, state in game_states:
            try:
                game = cls.__all_connected_games[game_id]
            except KeyError as ex:
                raise WebsocketNetworkAdaptorException('While trying to send all game state updates to players, the game_states provided includes an instance of a game not in all_connected_games.') from ex
            tasks.append(game.send_current_state(state, ev_wrap=True))

        # ... and awaits completion of all group_send  orders before proceeding.
        asyncio.gather(*tasks, return_exceptions=True)
        # Handle exceptions ...

    
    async def send_current_state(self, state, ev_wrap=False):
        '''
            [DO NOT USE ON ITS OWN] Send game state to all players of this game group.
            This sends the state to each groupe sequentialy and awaits after 
            each group_send call.
        '''
        if not state:
            raise ValueError('Trying to send empty state to client.')
        
        if ev_wrap:
            state = {
                'ev': 'up',
                'state': state
            }

        payload = json.dumps(state)
        await self.consumer.channel_layer.group_send(self.__game_id,
                {
                    'type': 'game.send.state',
                    'game_state': payload
                }
        )
    

    def add_player(self, uid: int, consumer: GameConsumer, event=None):
        '''  '''
        if uid and (uid in self.__connected_players):
            raise WebsocketNetworkAdaptorException('Failed to add player to GameConnector : Is already member.')
        self.__connected_players[uid] = PlayerConnector(consumer)



    def push_player_event(self, event):
        ''' Called by the WebsocketNetworkAdaptor as player events are received
         from GAME_CONN typed websockets. Received events are pushed into the 
         specific GameConnector's queue in which the player is currently a 
         member. '''
        if not event:
            return
        self.__player_events.put(event)
        


    def get_player_event(self):
        ''' Called by GameManager to get latest player events from the queue. 
         Can be called repeatedly until event queue is empty and returns None.'''
        if self.__player_events.empty():
            return None
        return self.__player_events.get()
    

    async def kick_player(self, uid: int):
        if uid not in self.__connected_players:
            raise WebsocketNetworkAdaptorException(f"The user id of the player you tried to kick out {uid} does not exist in game {self.__game_id}.")
        player = self.__connected_players[uid]
        await player.send_disconnect_signal()
"""

        

   
"""
class NotificationConnector(BaseGateway):
    ''' Theoretical notification connector '''
    pass




class WebsocketNetworkAdaptorException(Exception):
    pass


class WebsocketNetworkAdaptor:
    ''' 
        Singleton class managing throughput between Websocket consumer 
     and GameManager. 

        A player can be added to multiple websocket types on the server.
     Most common one being the 'player_conn' websocket connection,
     used to receive player moves during a game and to send game state updates.
     But other type of websocket connections could be useful; 
     such as a 'notif_conn' notification channel to send friend invites
     to games or tournaments, or live data feed to update some frontend 
     component; such as a list of live tournaments for exemple.
     The self.__connected_users dict takes the user.id as key and the value
     is a dict of connection services the user can connect to. See below :

     self.__connected_users = {
        <user_id>: {
            GAME_CONN: None,
            NOTIF_CONN: None,
            '[some service]_conn': None,
            ...
        }
        ...
     }


    '''

    #/// Connector type Enums
    GAME_CONN = 1
    NOTIF_CONN = 2
    #////////////////////////

    #__default_conn_types = {
    #        GAME_CONN: None,
    #        NOTIF_CONN: None
    #    }
    
    __connector_types = {
        #GAME_CONN: PlayerConnector,
        GAME_CONN: GameConnector,
        NOTIF_CONN: NotificationConnector,
    }

    def __init__(self):
        self.__connected_users = dict()

    def __is_connected_to_service(self, uid: int, service) -> bool:
        return (
            uid in self.__connected_users
            and service in self.__connected_users[uid]
            and self.__connected_users[uid][service] is not None
        )

    #def connect_user_as_player(self, consumer: GameConsumer, user: User) -> PlayerConnector:
    def connect_user_to_service(self, consumer: AsyncWebsocketConsumer,
                                user: User, service: int, *args, **kwargs) -> PlayerConnector:
        ''' The service argument is one of the enums define at the class level. '''

        uid = user.id

        if self.__is_connected_to_service(uid, self.GAME_CONN):
            raise WebsocketNetworkAdaptorException(f'User {uid} ({user.username}) already connected as player. Disconnect from current game before connecting to new one.')

        # If user is not known to the network adaptor, initialize an empty list
        # to its id in self.__connected_users. This list will contain the live feed
        # services to which they are subscribed. If the user disconnects from a service,
        # the connector instance should be removed from self.__connected_users
        # and propperly disconnected and deleted.
        self.__connected_users.setdefault(uid, [])
        selected_service = self.__connector_types[service]
        connector = selected_service(consumer, user, *args, **kwargs)
        self.__connected_users[uid].append(connector)





#WS_NET = WebsocketNetworkAdaptor()
"""