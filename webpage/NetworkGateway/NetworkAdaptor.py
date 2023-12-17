
from abc import ABC
import json
import sys

from channels.layers import get_channel_layer

from users.models import User
from queue import Queue
import asyncio
import time
from NetworkGateway.consumers import GameConsumer
from NetworkGateway.models import GameEvent
from game.models import Game
import game.PingPongRebound.defs as df
from asgiref.sync import sync_to_async, async_to_sync
from tournament.consumers import TournamentConnector
from tournament.models import Tournament
from tournament.LiveTournament import LiveTournament

def eprint(*args):
    print(*args, file=sys.stderr)

class BaseGateway(ABC):
    pass
class GameGatwayException(Exception):
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
        self.lobby_game = None # Returned after connecting to MatchMaker
        self.__events = asyncio.Queue()
        self.__scores: list = []

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

    #  SETTER  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def set_lobby_game(self, lgame):
        if self.lobby_game and lgame != self.lobby_game:
            GameGatwayException('Trying to set game_connector.lobby_game to different game. lobby_game can only be set once.')
        self.lobby_game = lgame
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
        print("push_event: ", event)
        async with self.__events_lock:
            await self.__events.put(event)
            print('event queue length : ', self.__events.qsize())

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
        print('CALLED send_end_state()')
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
    async def disconnect_player(self, user):
        print(f'GameConnector :: ENTER disconnect player')
        if not self.lobby_game:
            return None
        async with self.__game_lock:
            if user.id not in self.__player_consumers:
                raise ValueError(f"Trying to disconnect user {user.login} from a game they don't belong to.")
            consumer = self.__player_consumers.pop(user.id)
        await self.__channel_layer.group_discard(self.__sockID, consumer.channel_name)
        print(f'GameConnector :: SWITCH')
        if self.game:
            print(f'GameConnector :: disconnect player {user.id} INGAME')
             # send disconnect event to Game instance in game manager. Same place as keypress events.
            await self.push_event(user.id, 'end_game')
        elif self.nb_connected > 0:
            print(f'GameConnector :: disconnect player {user.id} while IN LOBBY')
            # send updated player list to all players without the disconnected player
            await self._send_players_list()
        else:
            print('WTF DUDE !! async def disconnect_player(self, user), other')
    # async def disconnect_all_players(self):
    #     # async with self.__game_lock:
    #     #     for ply in self.__player_consumers:
    #     pass

    # INFORMATION SENDING EVENT  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Get all players as a list
    async def _send_players_list(self):
        async with self.__game_lock:
            # Players list from lobby_game
            players = self.lobby_game.players
        # Payload to send to all players
        payload = [ { 'login': ply.user.login, 'img': ply.user.img_link, 'ready': ply.is_ready }
            for ply in players ]
        print('send player info payload : ', payload)
        await self.__channel_layer.group_send(
            self.__sockID,
            {
                'type': 'game_new_connection_message',
                'players': payload
            }
        )
    # Send start signal to SOCKID
    async def send_start_signal(self):
        print('<<< SENDING START SIGNAL !! >>>')
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




# Singleton object which orchestrats the sending of updates to all games
class GameGateway(BaseGateway):
    def __init__(self):
        GameConnector.set_game_gateway(self)
        self.__channel_layer = get_channel_layer()
        self.__match_maker = None# Must be setup with self.set_matchmaker() before accepting connections
        self.__game_manager = None# Must be setup with self.set_gamemanager() before accepting connections
        self.__gateway_lock = asyncio.Lock()

        # TOURNAMENT
        # There can only be one live tournament going on at the same time
        self._live_tournament: LiveTournament = None

    @property
    def match_maker(self):
        return self.__match_maker

    #  SETTER  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def set_match_maker(self, match_maker):
        #In setup phase, in GameConfig.ready()
        if self.__match_maker:
            raise ValueError('Can only be setup once')
        self.__match_maker = match_maker

    def set_game_manager(self, game_manager):
        if self.__game_manager:
            raise ValueError('Can only be setup once')
        self.__game_manager = game_manager


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

        if lobby_game.is_tournament:
            ''' Tournament lobby games from MatchMaker are pseudo lobbies to be overwritten by the LiveTournament
             instance. Only  '''
            if self._live_tournament:
                raise GameGatwayException('Their can only be one tournament running at the same time. Try again later.')
            if not lobby_game.tour_connector:
                tconn = TournamentConnector('Tour::' + sockID)
                self._live_tournament = LiveTournament(tconn, lobby_game)
                lobby_game.set_tour_connector(tconn)
            else:
                tconn = lobby_game.tour_connector

            brackets = self._live_tournament.get_brackets_info()
            await tconn.send_brackets(brackets)


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

    async def disconnect_player(self, user: User, consumer):
        ''' This method should only be used to disconnect players while in lobby. '''

        print('GameGateway trying to disconnect player')
        gconn = consumer.game_connector
        if user in self.match_maker:
            print('\nTry remove and disconnect player in Lobby inside MatchMaker.')
            async with self.__gateway_lock:
                rem = self.match_maker.remove_player(user)
            lgame, lply = rem
            if not lgame.is_empty:
                await gconn.disconnect_player(user)
                #lgame.game_connector._send_players_list()

        elif (gconn is not None):
            print('\nTry remove and disconnect player IN GAME.')
            await gconn.disconnect_player(user)
            consumer.user = None
            consumer.game_connector = None

        else:# Disconnect if in tournament
            print('Trying to disconnect but GOT ELSED !')

    ### DEBUG VERSION :
    official_gameModes = {'Local_1p', 'Multiplayer', 'Tournament', 'Online_4p'}
    ### PRODUCTION VERSION :
    # official_gameModes = {'Multiplayer', 'Tournament', 'Online_4p'}

    def __is_official_gameMode(self, gameMode):
        return gameMode in self.official_gameModes

    gameModeEnums = {
        'Local_1p': df.SOLO,
        'Local_2p': df.DUAL,
        'Multiplayer': df.FREEPLAY,
        'Online_4p': df.FREEPLAY,
        'Tournament': df.TOURNAMENT
    }

    # @sync_to_async
    # def __create_db_tounrament(self, lgame, gameType, maxPlayers):#, **kwargs):
    #     game = Game.objects.create(
    #         game_type=gameType,
    #         max_players=maxPlayers,#self._maxRacketCounts[gameType]
    #         is_official=self.__is_official_gameMode(lgame.gameMode)
    #     )
    #     for lply in lgame.players:
    #         game.add_player(lply.user, save=False)
    #     game.declare_started(save=True)
    #     lgame.game_connector.set_game_db_instance(game)
    #     return game

    @sync_to_async
    def __create_db_game(self, lgame, gameType, maxPlayers):#, **kwargs):
        game = Game.objects.create(
            game_type=gameType,
            max_players=maxPlayers,#self._maxRacketCounts[gameType]
            is_official=self.__is_official_gameMode(lgame.gameMode)
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
        game = await self.__create_db_game(lgame, gameType, self.__game_manager.getMaxPlayerCount(gameType))

        self.match_maker.remove_lobby_game(lgame)

        GameManagerMode = self.gameModeEnums.get(lgame.gameMode, None)
        if not GameManagerMode:
            raise TypeError('Trying to push game to GameManager with invalid gameMode')

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

        await lgame.game_connector.send_start_signal()
        await gm.startGame(lgame.sockID)

        return lgame


    async def set_player_ready(self, user: User):
        ''' Called from a sync HTTP POST request, so no reference to lobby_game
        or game_connector unlike websocket messages with consumer. '''
        print(f"\n\nTrying to set user {user.id} as ready")
        async with self.__gateway_lock:
            lgame = self.match_maker.set_ready(user)

        if not lgame:
            raise GameGatwayException(f"Trying to set user {user.login} as ready, but wasn't found in lobby.")

        await lgame.game_connector._send_players_list()
        print('Checking if game is ready ?')
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



    async def manage_end_game(self, end_game_state: dict):
        ''' Will deal with either individual games or tournament games. Called by GameManager at the end of a game. '''
        print('\n\n !!!! WOWOW MANAGING END GAME !!!\n\n')
        print('END GAME : ', end_game_state)

        if not end_game_state:
            raise GameGatwayException("GameManager didn't give a propper end_game_state state struct to manage end game.")


        endState = end_game_state.get("endState", None)
        scores = end_game_state.get("scores", None)
        gameMode = end_game_state['gameMode']

        gconn = end_game_state.pop('gameConnector')
        game = gconn.game

        eprint('gameMode : ', gameMode)
        eprint('endState : ', endState)

        if endState == 'quit':
            eprint('endState == quit indeed')
            quitter = end_game_state['quitter']
            eprint('game was quit by playerID ', quitter)
            res = await game.stop_and_register_results(scores, quitter=quitter)
            eprint('db push res : ', res)
        elif endState == 'win':
            eprint('endState == win indeed')
            res = await game.stop_and_register_results(scores)
            eprint('db push res : ', res)
        elif endState == 'crash':
            eprint('endState == crash indeed')
        else:
            eprint("WTF DUDE !!! ")


        eprint('manage_end_game :: Trying to call gconn.send_end_state with endState : ')
        eprint("endState : ", end_game_state)
        await gconn.send_end_state(end_game_state)
        eprint('manage_end_game :: post send_end_state')

        # stop_and_register_results
        eprint('EXITING manage_end_game()')


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