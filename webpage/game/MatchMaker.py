from dataclasses import dataclass
from users.models import User
# from game.models import Game
from game.forms import GameCreationForm
#from game.PingPongRebound import Pong, Ponger, Pongest, Pongester, Ping, Pinger, Pingest
#from game.PingPongRebound import GameManager as gm#Po, Pi, Pong, Ping, Ponger, Pinger, Pongest, Pingest
#from game.PingPongRebound import GameManager
import asyncio
#from asgiref.sync import sync_to_async

''' We can assume this msg struct is correct since the frontend UI
can only propose valid choices. '''
test_join_msg = {
    'gameMode': 'Freeplay',
    'gameType': 'Pong'
}

class MatchMakerException(Exception):
    pass
class MatchMakerWarning(Warning):
    pass

@dataclass
class LobbyPlayer:
    user: User
    is_connected: bool
    is_ready: bool


# @dataclass
# class LobbyGame:
#     form: GameCreationForm
#     players: list[LobbyPlayer]

class LobbyGame:
    __id_counter = 0
    __maxPlayerCounts = None # Set by MatchMaker through set_maxPlayerCounts().

    @classmethod
    def __get_lobby_id(cls):
        cls.__id_counter += 1
        return cls.__id_counter

    @classmethod
    def set_maxPlayerCounts(cls, maxPlayerCounts: dict):
        if not (maxPlayerCounts and isinstance(maxPlayerCounts, dict)):
            raise TypeError('Set maxPlayerCounts takes a dict of nb of players required for eauc gameType.')
        cls.__maxPlayerCounts = maxPlayerCounts


    def __init__(self, form: GameCreationForm, players: list[LobbyPlayer]):

        self.__id: int = self.__get_lobby_id()
        self.__form: GameCreationForm = form
        self.__players: list[LobbyPlayer] = players
        self.__required_players: int = self.__maxPlayerCounts[self.gameType]
        #self.__is_started: bool
        self.__game_connector = None # Set by GameGateway after successfull join_game() call with instance of GameConnector object.
        self.__tour_connector = None # Set by GameGateway after successfull join_game() call with instance of TournamentConnector object. Only set if gameMode == 'Tournament'.
        # self.__tournament = None


    def __repr__(self):
        return f"LobbyGame<id: {self.lobbyID}, form: {self.form}, players: {self.player_names}>"

    def __contains__(self, user: User):
        return next((lply for lply in self.__players if user == lply.user), None)
        #return next(filter(lambda lply: user == lply.user, self.__players), None)
        #return any(user == lply.user for lply in self.__players)

    @property
    def lobbyID(self):
        return self.__id
    @property
    def sockID(self):
        return "sock{:06d}".format(self.__id)
    @property
    def tourID(self):
        # if not self.__tour_connector:
        #     return None
        return f'Tour_{self.sockID}'
    @property
    def form(self):
        return self.__form
    @property
    def gameType(self):
        return self.__form['gameType']
    @property
    def gameMode(self):
        return self.__form['gameMode']
    @property
    def eventID(self):
        return self.__form['eventID']
    @property
    def withAI(self):
        return self.__form['withAI'] == 'True'
    @property
    def players(self):
        return self.__players
    @property
    def player_names(self):
        return [lply.user.display_name for lply in self.__players]
    @property
    def nb_players(self):
        return len(self.__players)
    @property
    def game_connector(self):
        return self.__game_connector
    @property
    def tour_connector(self):
        return self.__tour_connector
    @property
    def is_ready(self) -> bool:
        print('-> Game Lobby is_ready check :')
        print('-> is_full : ', self.is_full)
        print('-> Players connected and ready status : ', [lply.is_connected and lply.is_ready for lply in self.__players])

        return self.is_full and all(lply.is_connected and lply.is_ready for lply in self.__players)
    @property
    def is_full(self):
        if self.gameMode == 'Tournament':
            return (len(self.__players) == 4)
            # return (len(self.__players) == 2)
        if (self.withAI or (self.gameMode == 'Local_2p')) and (len(self.__players) > 0):
            return True
        return self.nb_players == self.__required_players
    @property
    def is_empty(self):
        return not self.__players
    @property
    def is_tournament(self):
        return self.gameMode == 'Tournament'
    @property
    def is_tournament_game(self):
        return self.eventID != '0' 

    def set_game_connector(self, gconn):
        self.__game_connector = gconn
    def set_tour_connector(self, tconn):
        self.__tour_connector = tconn

    def add_player(self, lply: LobbyPlayer):
        if not (lply and isinstance(lply, LobbyPlayer)):
            raise TypeError('lply should be and instance of LobbyPlayer')
        if self.is_full:
            raise MatchMakerException('Trying to add player to an already full game.')
        if lply in self.__players:
            raise MatchMakerException('Trying to add player to the same game twice.')
        self.__players.append(lply)

    def set_player_ready(self, user: User):
        if not (lply := (user in self)):
            raise MatchMakerWarning(f'Tryin to set user {user.login} as ready in game {self.lobbyID}, but this player is not in this game.')
        lply.is_ready = True
        return lply
    
    def set_event_id(self, eventID):
        self.__form['eventID'] = eventID

    def get_player(self, user: User):
        cantidates = [lply for lply in self.__players if lply.user.id == user.id]
        if not cantidates:
            return None
        return cantidates[0]

    def remove_user(self, user: User):
        for i, lply in enumerate(self.__players):
            if user == lply.user:
                break
        else:
            return None
        return self.__players.pop(i)


    def remove_player(self, lply: LobbyPlayer):
        for i, p in enumerate(self.__players):
            if p == lply:
                break
        else:
            return None
        return self.__players.pop(i)
        #index = -1
        #for i, lply in enumerate(self.__players):
        #    if lply.user == user:
        #        index = i
        #        break
        #else:
        #    return None
        #return self.__players.pop(index)


class MatchMaker:

    _maxRacketCounts = dict()

    def __init__(self, game_manager = None):

        self.gm = game_manager

        self._gameLobby = {
            'Tournament': [],
            'Multiplayer': [],
            'Online_4p': [],
            'Local_1p': [],
            'Local_2p': []
        }

        if not MatchMaker._maxRacketCounts:
            MatchMaker._maxRacketCounts['Pong'] = self.gm.getMaxPlayerCount('Pong')
            MatchMaker._maxRacketCounts['Ping'] = self.gm.getMaxPlayerCount('Ping')
            MatchMaker._maxRacketCounts['Pingest'] = self.gm.getMaxPlayerCount('Pingest')
            LobbyGame.set_maxPlayerCounts(MatchMaker._maxRacketCounts)
            # _maxRacketCounts = {
            #     #'Pi': self.gm.getMaxPlayerCount('Pi'),
            #     'Ping': self.gm.getMaxPlayerCount('Ping'),
            #     #'Pinger': self.gm.getMaxPlayerCount('Pinger'),
            #     'Pingest': self.gm.getMaxPlayerCount('Pingest'),
            #     #'Po': self.gm.getMaxPlayerCount('Po'),
            #     'Pong': self.gm.getMaxPlayerCount('Pong'),
            #     #'Ponger': self.gm.getMaxPlayerCount('Ponger'),
            #     #'Pongest': self.gm.getMaxPlayerCount('Pongest'),
            # }


    def __contains__(self, user: User):
        return self.has_player(user)

    def has_game(self, gameID):
        pass
    def has_player(self, user: User):
        return self.__find_player_in_lobby(user) is not None
    
    def get_tournament(self):
        if not self._gameLobby['Tournament']:
            return None
        return self._gameLobby['Tournament'][0]


    # def is_game_full(self, gameType: str, lgame: LobbyGame):
    #     print("MatchMaker Checking is_game_full with gameType : ", gameType)
    #     return len(lgame.players) == self._maxRacketCounts[gameType]

    # def is_game_ready(self, lgame: LobbyGame):

    #     # Thi should change if AI games with more
    #     # then 2 players are allowed.
    #     if lgame.withAI and lgame.players and lgame.players[0].is_ready:
    #         return True

    #     return self.is_game_full(lgame.gameType, lgame)\
    #         and all(lply.is_ready for lply in lgame.players)


    def __find_existing_game_such_as(self, user: User, form: GameCreationForm|dict):

        for lgame in self._gameLobby[form['gameMode']]:
            for lply in lgame.players:
                # if user == lply.user:
                #     raise MatchMakerWarning(f'User {user.login} tried to join a game twice. Stop that !')
                if not lgame.is_full and form == lgame.form:
                #if not self.is_game_full(form['gameType'], lgame) and form == lgame.form:
                    return lgame
        return None

    def __find_player_in_lobby(self, user: User) -> LobbyGame|None:
        print('Trying __find_player_in_lobby with user : ', user.login)
        for gameMode, typedGames in self._gameLobby.items():
            for lgame in typedGames:
                #if (lply := (user in lgame)):
                #    return (gameMode, lgame, lply)
                #if user in lgame:
                for lply in lgame.players:
                    if user == lply.user:
                        print(f'Game containing user {user.login} FOUND ')#: ', lgame)
                        return (gameMode, lgame, lply)

        print('No Game found containing user : ', user.login)
        return None
    
    def __find_event_in_lobby(self, user: User, eventID: str) -> LobbyGame|None:
        print('Trying __find_event_in_lobby with eventID : ', eventID)
        for gameMode, typedGames in self._gameLobby.items():
            for lgame in typedGames:
                if lgame.eventID == eventID:
                    print(f'Game {eventID} FOUND ')#: ', lgame)
                    return (gameMode, lgame, lgame.get_player(user))

        print('No Game found containing user : ', user.login)
        return None


    def remove_lobby_game(self, lgame: LobbyGame):
        ''' Begore removing game from lobby prior to adding game in GameManager,
        make sure to keep a ref outside to extract its GameConnector instance to
        pass to GameManager. '''
        game_mode = lgame.gameMode
        modeGames = self._gameLobby[game_mode]
        if lgame not in modeGames:
            raise MatchMakerException(f"Trying to remove game {lgame} from the lobby but this game does not exist in MatchMaker.")

        modeGames.remove(lgame)
        #game_type = lgame.gameType
        #if not game_type or not game_type in self._gameLobby:
        #self._gameLobby[game_type].remove(lgame)

    # @sync_to_async
    # def __create_db_game(self, lgame: LobbyGame, gameType, maxPlayers):#, **kwargs):
    #     game = Game.objects.create(
    #         game_type=gameType,
    #         max_players=maxPlayers#self._maxRacketCounts[gameType]
    #     )
    #     for lply in lgame.players:
    #         game.add_player(lply.user)
    #     game.declare_started()
    #     return game

    # async def __push_game_to_gamemanager(self, gameType: str, lgame: LobbyGame):
    #     ''' When calling this function, the game should be validated ready to start. '''
    #     game = await self.__create_db_game(lgame, gameType, self._maxRacketCounts[gameType])
    #     #game = sync_to_async(Game.objects.create)()
    #     #        game_type=gameType,
    #     #        max_players=self._maxRacketCounts[gameType]
    #     #    )
    #     #)
    #     print('game after sync_to_async db game creation : ', game)
    #     gm_status = await self.gm.addGame(gameType, game.id)
    #     if not gm_status:
    #         raise MatchMakerException('Error occured while trying to create new game in game_manager.')


    #     #tasks = [self.gm.addPlayerToGame(lply.user.id, lply.user.login, game.id) for lply in lgame.players]
    #     #await asyncio.gather(tasks)
    #     for lply in lgame.players:
    #         await self.gm.addPlayerToGame(lply.user.id, lply.user.login, game.id)
    #     await self.gm.startGame(game.id)
    #     lgame.set_is_started()
    #     self.__remove_lobby_game(lgame)
    #     return lgame

    #COLLE
    # recois le form ici
    def join_lobby(self, user: User, form: GameCreationForm|dict):
        ''' Can accept either GameCreationForm.cleaned_data objects or
        popperly formated dict with valid entries for "gameMode" and "gameType".
        Then, if valid, instanciates the game in the database and puts  '''

        gameMode = form.get('gameMode')
        gameType = form.get('gameType')
        if not gameMode or not gameType:
            raise ValueError('Missing one or more fields in form.')
        if gameMode not in self._gameLobby:
            raise ValueError(f"Game Mode {gameMode} does not exit.")
        
        lgame = self.__find_existing_game_such_as(user, form)

        lply = LobbyPlayer(user=user, is_connected=False, is_ready=False)
        if lgame:
            if user in lgame:
                raise MatchMakerWarning(f'User {user.login} tried to join a game twice. Stop that !')
            if lgame.is_tournament and lgame.is_full:
                raise MatchMakerWarning(f"Cannot start new tournament while another one is happening. Try again later.")

            # Game should be fully validated at this point
            lgame.add_player(lply)
            #lgame.players.append(lply)
        else:
            lgame = LobbyGame(form=form, players=[lply])
            self._gameLobby[gameMode].append(lgame)
            print("Match Maker Game Lobby : ", self._gameLobby)

        return lgame


    def connect_player(self, user: User, eventID: str = None):
        ''' Called by websocked when player connects to the games websocker with lobbyID
            after having called join_lobby() first, but before the game has officialy
            been created. '''
        
        if eventID:
            finder_result = self.__find_event_in_lobby(user)
        else:
            finder_result = self.__find_player_in_lobby(user)
        #print('finder_result : ', finder_result)
        if not finder_result:
            return None
        gameMode, lgame, lply = finder_result
        lply.is_connected = True

        ### DEBUG ONLY
        # print('Try set player ready ...')
        #if not await self.set_ready(user):
        #    return None
        # print('Player supposed to be ready')
        ##lply.is_ready = True ### DEBUG ONLY
        ### DEBUG ONLY

        print('gameMode, gameType, lgame, lply: ', gameMode, lgame.gameType, lgame, lply)

        print(f'User {user.login} was SUCCESSFULLY connected !')
        #if self.is_game_ready(lgame):
        #    asyncio.run(self.__push_game_to_gamemanager(lgame.gameType, lgame))
        return lgame

    # async def set_ready_player(self, lgame: LobbyGame, lply: LobbyPlayer):
    #     print(f'Setting player {lply.user.login} as READY !')
    #     lply.is_ready = True

    #     return lgame.is_ready #self.is_game_ready(lgame):
        #print('GAME is ready. Starting game ...')
        #return await self.__push_game_to_gamemanager(lgame.gameType, lgame)
        #ev_loop = asyncio.get_running_loop()
        #ev_loop.run_until_complete(self.__push_game_to_gamemanager(lgame.gameType, lgame))
        #asyncio.run(self.__push_game_to_gamemanager(lgame.gameType, lgame))
        #return lply

    def set_ready(self, user: User):
        finder_result = self.__find_player_in_lobby(user)
        if not finder_result:
            print('Player not in lobby while setting ready.')
            return None
        gameMode, lgame, lply = finder_result
        lply.is_ready = True
        return lgame
        #return self.set_ready_player(lgame, lply)



    def remove_player(self, user: User):
        #gameType, lgame, lply = self.__find_player_in_lobby(user)
        finder_result = self.__find_player_in_lobby(user)
        if not finder_result:
            return None
        gameMode, lgame, lply = finder_result
        if lgame.nb_players == 1:
            self.remove_lobby_game(lgame)
            #self._maxRacketCounts[lgame.gameType].remove(lgame)
        else:
            lgame.remove_player(lply)
            #lgame.players.remove(lply)
        return (lgame, lply)

