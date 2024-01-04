
from abc import ABC
import json
import sys

from channels.layers import get_channel_layer

from users.models import User
import asyncio
from game.models import Game
import game.PingPongRebound.defs as df
from asgiref.sync import sync_to_async
from tournament.TournamentConnector import TournamentConnector
from tournament.models import Tournament
from tournament.LiveTournament import LiveTournament
from game.apps import GameConfig as app
from game.MatchMaker import MatchMakerWarning
from NetworkGateway.GameConnector import GameConnector


def eprint(*args):
    print(*args, file=sys.stderr)


class BaseGateway(ABC):
    pass
class GameGatewayException(Exception):
    pass
class GameAPIException(Exception):
    pass


# Singleton object which orchestrats the sending of updates/connections/disconnections to all games
class GameGateway(BaseGateway):
    def __init__(self):
        GameConnector.set_game_gateway(self)
        LiveTournament.set_gameconnector_initializer(GameConnector)

        self.__channel_layer = get_channel_layer()
        self.__match_maker = None# Must be setup with self.set_matchmaker() before accepting connections
        self.__game_manager = None# Must be setup with self.set_gamemanager() before accepting connections
        self.__gateway_lock = asyncio.Lock()

        ## Holds a ref to all live game_connectors, so that synchronous API calls can reference
        # live games and send events after authentication. Takes userID as key and GameConnector as value.
        self.__game_connectors = dict()

        self.__event_loop = None

        # TOURNAMENT
        # There can only be one live tournament going on at the same time
        self._live_tournament: LiveTournament = None

    @property
    def match_maker(self):
        return self.__match_maker
    @property
    def event_loop(self):
        return self.__event_loop

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

    @property
    def is_tournament_started(self):
        return self._live_tournament is not None


    # def join_lobby(self, user: User, form: GameCreationForm|dict):
    async def join_game(self, user: User, form: dict):
        match_maker = app.get_match_maker()
        print(match_maker)

        if self._live_tournament is not None:
            return (False, "There already is a tournament running. Try again later.")

        try:
            lobby_game = match_maker.join_lobby(user, form)
        except MatchMakerWarning as w:
            return (False, w)

        if not lobby_game:
            return (False, 'Joining game lobby failed.')
        return (True, lobby_game)


    async def find_lobby_game_on_server(self, user: User):
        lobby_game = None
        # is_tournament_stage = False
        async with self.__gateway_lock:
            eprint('Entered lock')
            eprint('current live tournament : ', self._live_tournament)
            if self._live_tournament and user in self._live_tournament:
                # if self._live_tournament.first_stage_started:
                #     lobby_game = self._live_tournament.get_player_game(user)
                #     # is_tournament_stage = True
                # else:
                #     eprint('User is member of live tournament and live tournament exists.')
                lobby_game = self._live_tournament.connect_player(user)
                    # is_tournament_stage = True
                    # await self._live_tournament.connect_player(user, consumer)
            else:
                eprint('User is NOT member of live tournament game.')
                lobby_game = self.__match_maker.connect_player(user)
            eprint('Exit lock')

        return lobby_game


    async def connect_player(self, sockID, consumer):
        ''' Called by websocket consumer connect() method. '''

        if not self.__event_loop:
            self.__event_loop = asyncio.get_event_loop()

        eprint('\n\n GameGateway :: connect_player() entered ')
        if not (self.__game_manager or self.__match_maker):
            raise ValueError('MatchMaker and GameManager must be set before accepting connections.')

        user = consumer.user
        async with self.__gateway_lock:
            if self._live_tournament and user in self._live_tournament:
                lobby_game = self._live_tournament.connect_player(user)
            elif user in self.__match_maker:
                lobby_game = self.__match_maker.connect_player(consumer.user)

        eprint('\n\n GameGateway :: connect_player() before entering lock. ')

        if not lobby_game:
            raise GameGatewayException(f'User {consumer.user} connection to game FAILED !')

        eprint('GameGateway :: connect_player() :: self._live_tournament : ', self._live_tournament)
        # lobby_game.set_player_connected(consumer.user)

        ## Get or create game_connector
        if not lobby_game.game_connector:
            gconn = GameConnector(sockID)
            lobby_game.set_game_connector(gconn)
            gconn.set_lobby_game(lobby_game)
        else:
            gconn = lobby_game.game_connector
        async with self.__gateway_lock:
            userApiKey = user.apiKey
            if userApiKey not in self.__game_connectors:
                self.__game_connectors[userApiKey] = gconn

        eprint('GameGateway :: connect_player() :: gconn : ', gconn)
        eprint('GameGateway :: connect_player() :: gconn.connect_player() and send_init_state()')

        await gconn.connect_player(consumer.user, consumer)#, is_tournament_stage=is_tournament_stage)
        await gconn.send_init_state(self.__game_manager.getInitInfo(lobby_game.gameType))

        ## Get or Create tournament connector (if is tournament), and send brackets.
        if lobby_game.is_tournament:
            eprint('GameGateway :: lgame isTournament')

            ## Init TournamentConnector
            if lobby_game.tour_connector:
                tconn = lobby_game.tour_connector
            else:
                tconn = TournamentConnector(lobby_game)
                lobby_game.set_tour_connector(tconn)
                eprint('connect_player : lobby_game tconn after setting it : ', lobby_game.tour_connector)
                eprint('connect_player : INITIALIZING live_tournament with sockID : ', lobby_game.tourID)

            ## Init LiveTournament
            # if lobby_game.is_full:
            #     raise GameGatewayException('Cannot join the tournament. It it full.')
            async with self.__gateway_lock:
                if not self._live_tournament:
                    self._live_tournament = LiveTournament(tconn, lobby_game, app.get_match_maker(), self.__game_manager)

                eprint('TRY SENDING BRACKETS INFO')
                await tconn.send_brackets(self._live_tournament.get_brackets_info())

        return gconn


    async def connect_to_tournament(self, user: User, consumer):
        ''' Tournament lobby games from MatchMaker are pseudo lobbies to be overwritten by the LiveTournament
            instance. Only acts as initLobby to gather 4 players for the tournament using the regular player update
        events. This pseud lobby will be sent to LiveTournament object to organize the tournament with the currently
        connected and ready players.

            At this point, it should be garanteed that there is only one tournament that can run at the same time.
        '''

        eprint('LiveTournament after player connect to tournament : ', self._live_tournament)

        async with self.__gateway_lock:
            lobby_game = self.__match_maker.get_tournament()

        if not lobby_game.is_tournament:
            raise GameGatewayException('Trying to connect player to tournament but there is no tournament lobby open.')
        eprint('connect_player : lobby_game.is_tournament : YES ')

        ## Init TournamentConnector
        if lobby_game.tour_connector:
            tconn = lobby_game.tour_connector
        else:
            tconn = TournamentConnector(lobby_game)
            lobby_game.set_tour_connector(tconn)
            eprint('connect_player : INITIALIZING live_tournament with sockID : ', lobby_game.tourID)

        ## Init LiveTournament
        async with self.__gateway_lock:
            # if lobby_game.is_full:
            #     raise GameGatewayException('Cannot join the tournament. It it full.')
            if not self._live_tournament:
                self._live_tournament = LiveTournament(tconn, lobby_game, app.get_match_maker(), self.__game_manager)

        # async with self.__gateway_lock:
        #     if not self._live_tournament:
        #         self._live_tournament = LiveTournament(tconn, lobby_game, app.get_match_maker())

        # async with self.__gateway_lock:
        #     print('connect_to_tournament :: Current Lobby Game : ', self._live_tournament)
        #     if not self._live_tournament:
        #         raise GameGatewayException('Trying to connect to tournament without active tournament running.')

        tconn = self._live_tournament.connector
        await tconn.connect_player(user, consumer)

        eprint('LiveTournament after player connect : ', self._live_tournament)
        brackets = self._live_tournament.get_brackets_info()
        print('connect_player :: Sending Tournament backets : ', brackets)
        if brackets:
            await tconn.send_brackets(brackets)

        return self._live_tournament


    async def disconnect_player(self, user: User, consumer):
        print('GameGateway trying to disconnect player')
        async with self.__gateway_lock:
            gconn = consumer.game_connector
            eprint('GameGateway :: disconnect_player :: self._live_tournament : ', self._live_tournament)
            eprint('GameGateway :: disconnect_player :: user in self._live_tournament : ', user in self._live_tournament)
            if self._live_tournament and user in self._live_tournament:
                shutdown = await self._live_tournament.disconnect_player(user)
                eprint('GameGateway :: disconnect_player :: disconnected player from live_tournament :: should shutdown ? ', shutdown)
                if shutdown:
                    del self._live_tournament
                    self._live_tournament = None

            elif user in self.match_maker:
                print('\nTry remove and disconnect player in Lobby inside MatchMaker.')
                rem = self.match_maker.remove_player(user)
                lgame, lply = rem
                if not lgame.is_empty:
                    await gconn.disconnect_player(user)

            elif (gconn is not None):
                ## Send an end_game signal to gameManager for the game played by player
                # which will trigger the end of the game in GameManager and send endState
                # to GameGateway.manage_end_game(). This is where the cleanup belongs.
                print('\nTry remove and disconnect player IN GAME.')
                await gconn.disconnect_player(user)
                # consumer.user = None
                # consumer.game_connector = None

            else:# Disconnect if in tournament
                print('Trying to disconnect player but GOT ELSED !')

            userApiKey = user.apiKey
            if userApiKey in self.__game_connectors:
                _ = self.__game_connectors.pop(userApiKey)


    ### DEBUG VERSION :
    official_gameModes = {'Multiplayer', 'Tournament', 'Online_4p'}
    ### PRODUCTION VERSION :
    # official_gameModes = {'Multiplayer', 'Tournament', 'Online_4p'}

    async def disconnect_tournament_member(self, user, consumer):

        async with self.__gateway_lock:
            if self._live_tournament and user in self._live_tournament:
                tourShutdown = await self._live_tournament.disconnect_player(user)
                if tourShutdown:
                    ### Do tournament shutdown procedure
                    del self._live_tournament
                    self._live_tournament = None

    def __is_official_gameMode(self, gameMode):
        return gameMode in self.official_gameModes

    gameModeEnums = {
        'Local_1p': df.SOLO,
        'Local_2p': df.DUAL,
        'Multiplayer': df.FREEPLAY,
        'Online_4p': df.FREEPLAY,
        'Tournament': df.TOURNAMENT
    }

    @sync_to_async
    def __create_db_tournament(self, initLobby):
        tour = Tournament.objects.create()
        # for lply in initLobby.players:
            # tour.add_member(lply.user, save=False)
        initLobby.tour_connector.set_tour_db_instance(tour)
        # return tour

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

        print('\n\n __push_game_to_gamemanager :: GameManagerMode : ',  GameManagerMode)
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
            raise GameGatewayException('Error occured while trying to create new game in game_manager.')

        tasks = [gm.addPlayerToGame(lply.user.id, lply.user.login, lgame.sockID) for lply in lgame.players]
        await asyncio.gather(*tasks)

        await lgame.game_connector.send_start_signal()
        await gm.startGame(lgame.sockID)

        return lgame

    async def __setup_live_tournament(self, initLobby):
        ''' Work in progress '''
        if self._live_tournament is None:
            raise GameGatewayException('GameGateway :: Trying to setup live tournament while no live tournament has been instanciated.')
        await self.__create_db_tournament(initLobby)

        ## Remove initLobby from match_maker only after the end of the tournament.
        # self.match_maker.remove_lobby_game(initLobby)
        tconn = initLobby.tour_connector
        gameA, gameB = await self._live_tournament.setup_game_lobbies_start()

        eprint('GameGateway :: __setup_live_tournament :: Trying to send_stage_initializer() to both game of stage 1.')
        await tconn.send_stage_initializer(gameA, 1)
        await tconn.send_stage_initializer(gameB, 1)
        eprint('GameGateway :: __setup_live_tournament :: Both game init should be sent.')
        # await self.__push_game_to_gamemanager('Pong', gameA)
        # await self.__push_game_to_gamemanager('Pong', gameB)


    ### READY
    async def set_player_ready(self, user: User):
        ''' Called from a sync HTTP POST request, so no reference to lobby_game
        or game_connector unlike websocket messages with consumer. '''

        print(f"\n\nTrying to set user {user.id} as ready")
        lgame = await self.find_lobby_game_on_server(user)
        if (not lgame):
            raise GameGatewayException(f'Trying to set player {user.login} as ready but player was not found on the server.')

        lgame.set_player_ready(user)
        # async with self.__gateway_lock:
        #     lgame = self.match_maker.set_ready(user)

        # if not lgame:
        #     raise GameGatewayException(f"Trying to set user {user.login} as ready, but wasn't found in lobby.")

        await lgame.game_connector._send_players_list()
        print('Checking if game is ready ?')
        if lgame.is_ready:
            eprint('lobby game IS ready.')

            if lgame.is_tournament:
                await self.__setup_live_tournament(lgame)
            else:
                ## SEND GAME TO GAME MANAGER
                print('\n\n GAME IS READY !!! ')
                print('SENDING GAME TO MANAGER !!! ')
                await self.__push_game_to_gamemanager(lgame.gameType, lgame)
                print(f"Lobby Game send to game manager : ", {lgame})
        else:
            eprint('lobby game IS NOT ready.')



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


    async def api_handle_event(self, userApiKey, eventType, key=None):
        ''' Methode called by sync HTTP api requests to send events to specific currently running game.'''
        async with self.__gateway_lock:
            if userApiKey not in self.__game_connectors:
                raise GameAPIException(f'API :: User sent event to API, but is not currently in a game.')
            gconn = self.__game_connectors[userApiKey]
            eprint(f'FOUND game connector associated to apiKey {userApiKey} !')

        user = await gconn.find_user_with_api_key(userApiKey)
        eprint(f'FOUND USER associated to apiKey {userApiKey} : login {user.login} !')
        if not user:
            raise GameAPIException(f'API :: User tried to execute action through API, but provided wrong API ID.')

        eprint(f'API call pushing event {key} to game event queue')
        await gconn.push_event(user.id, eventType, key)



    async def manage_end_game(self, end_game_state: dict):
        ''' Will deal with either individual games or tournament games. Called by GameManager at the end of a game. '''
        eprint('\n\n !!!! WOWOW MANAGING END GAME !!!\n\n')
        eprint('END GAME : ', end_game_state)

        if not end_game_state:
            raise GameGatewayException("GameManager didn't give a propper end_game_state state struct to manage end game.")


        endState = end_game_state.get("endState", None)
        scores = end_game_state.get("scores", None)
        gameMode = end_game_state.get('gameMode', None)

        gconn = end_game_state.pop('gameConnector')
        game = gconn.game
        lgame = gconn.lobby_game

        eprint('gameMode : ', gameMode)
        eprint('endState : ', endState)

        if endState == 'quit':
            quitter = end_game_state['quitter']
            eprint('endState == quit indeed. quitterID : ', quitter)
            user = await User.get_user(quitter)
            if user:
                # ply = lgame.get_player_by_id(quitter)
                end_game_state['wallofshame'] = user.img_link
                eprint('game was quit by playerID ', quitter)
                res = await game.stop_and_register_results(scores, quitter=quitter)
                eprint('db push res : ', res)
            else:
                await game.stop_and_register_force_close()
                return
                # raise GameGatewayException('GameGateway :: quitter id does not exist.')

        elif endState == 'win':
            eprint('endState == win indeed')
            res = await game.stop_and_register_results(scores)
            eprint('db push res : ', res)
        elif endState == 'abort':
            eprint('endState == abort indeed')
        else:
            eprint("WTF DUDE !!! ")


        # TODO: TOURNAMENT END GAME MANAGMENT
        if gconn.is_tournament_game:
            eprint('GameGateway :: managing end game while gconn.is_tournament_game is TRUE.')
            end_game_state['is_tournament'] = True


            # async with self.__gateway_lock:
            #     if self._live_tournament.is_first_stage:
            #         pass
            #     elif self._live_tournament.is_second_stage:
            #         pass



        eprint('manage_end_game :: Trying to call gconn.send_end_state')
        eprint('end_game_state : ', end_game_state)
        await gconn.send_end_state(end_game_state)
        eprint('manage_end_game :: post send_end_state')

        # stop_and_register_results
        eprint('EXITING manage_end_game()\n')


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