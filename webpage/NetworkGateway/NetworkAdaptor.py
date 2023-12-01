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

from consumers import GameConsumer
from user.models import User
from queue import Queue
import asyncio
import time
from functools import wraps




def async_to_sync_locked_class(func):
    @wraps(func)
    def __async_to_sync_game_locked(cls, *args, **kwargs):
        async def __game_locked_exec(args, kwargs):
            async with cls.__game_lock:
                func(cls, *args, **kwargs)
        asyncio.run(__game_locked_exec(args, kwargs))
    return __async_to_sync_game_locked


def async_to_sync_locked(func):
    @wraps(func)
    def __async_to_sync_game_locked(self, *args, **kwargs):
        async def __game_locked_exec(args, kwargs):
            async with self.__game_lock:
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
    def __init__(self, game_id, player_consumers):
        self.__channel_layer = get_channel_layer()
        self.__game_id = game_id
        self.__player_consumers = player_consumers

    def add_player(self, uid, consumer):
        if uid in self.__player_consumers:
            raise ValueError('Trying to add player to same game twice.')
        self.__player_consumers[uid] = consumer

    def diconnect_player(self, uid):
        ''' Used to kickout player forcefully '''
        pcons = self.__player_consumers[uid]
        asyncio.async_to_sync(self.__channel_layer.group_discard)(self.__game_id, pcons.channel_name)
    

class GameGatwayException(Exception):
    pass

class GameGateway(BaseGateway):
    ''' Singleton object which orchestrats the sending of updates to all games '''

    def __init__(self):
        self.__channel_layer = get_channel_layer()
        self.__connected_games[GameConnector] = dict()
        self.__game_lock = asyncio.Lock()

        self.__player_events = asyncio.Queue()

    @async_to_sync_locked
    def track_game(self, game_id, player_consumers):
        gconn = GameConnector(game_id, player_consumers)
        self.__channel_layer[game_id] = gconn

    @async_to_sync_locked
    def remove_game(self, game_id):
        if game_id in self.__connected_games:
            del self.__connected_game.pop(game_id)
    

    async def async_send_all_updates(self, game_states: dict[int, any], ev_wrap=False):
        async for game_id, state in game_states:
            async with self.__game_lock:
                
                if not state:
                    raise ValueError('Trying to send empty state to client.')
                
                if game_id not in self.__connected_games:
                    raise ValueError('Trying to send update to non-existant game_id.')

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
    
    def send_all_updates(self, game_states: dict[int, any], ev_wrap=False):
        asyncio.run(self.send_all_updates(game_states, ev_wrap))


    async def start_game_countdown(self, game_id):
        if game_id not in self.__connected_games:
            raise ValueError('Trying to send data to non-existant game_id.')
        
        event = {
            'ev': 'countdown',
            'counter': 3
        }

        for i in range(3):
            t_start = time.monotonic()
            payload = json.dumps(event)
            await self.__channel_layer.group_send(game_id,
                {
                    'type': 'game.send.state',
                    'payload': payload
                }
            )
            payload['counter'] -= 1
            dt = time.monotonic() - t_start
            await asyncio.sleep(1.0 - dt)





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





WS_NET = WebsocketNetworkAdaptor()
