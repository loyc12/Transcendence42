from dataclasses import dataclass
from users.models import User
from game.forms import GameCreationForm

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
        self.__game_connector = None # Set by GameGateway after successfull join_game() call with instance of GameConnector object.
        self.__tour_connector = None # Set by GameGateway after successfull join_game() call with instance of TournamentConnector object. Only set if gameMode == 'Tournament'.
        # self.__tournament = None
        self.__winnerID = None


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
    def game(self):
        if self.__game_connector:
            return self.__game_connector.game
        return False
    @property
    def tour_connector(self):
        return self.__tour_connector
    @property
    def is_ready(self) -> bool:
        print('-> Game Lobby is_ready check :')
        print('-> is_full : ', self.is_full)
        print('-> Players connected and ready status : ', [{'CONNECTED': lply.is_connected, 'READY': lply.is_ready} for lply in self.__players])

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
    @property
    def is_live_tournament(self):
        return self.is_tournament and self.tour_connector and self.tour_connector.is_running
    @property
    def is_running(self):
        return self.game_connector is not None and self.game_connector.game is not None and self.game_connector.game.is_running
    @property
    def is_over(self):
        return self.game_connector is not None and self.game_connector.game is not None and self.game_connector.game.is_over
    @property
    def winner(self):
        if not (self.__game_connector is not None and self.__game_connector.game is not None and self.__game_connector.game.winner):
            return None
        return self.__game_connector.game.winner

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

    def set_player_connected(self, user: User):
        for lply in self.__players:
            if lply.user.id == user.id:
                break
        else:
            raise MatchMakerWarning(f'Tryin to set user {user.login} as connected in game {self.lobbyID}, but this player is not in this game.')
        # if not (lply := (user in self)):
        lply.is_connected = True
        return lply

    def set_player_ready(self, user: User):
        for lply in self.__players:
            if lply.user.id == user.id:
                break
        else:
            raise MatchMakerWarning(f'Tryin to set user {user.login} as ready in game {self.lobbyID}, but this player is not in this game.')
        # if not (lply := (user in self)):
        lply.is_ready = True
        return lply

    def set_event_id(self, eventID):
        self.__form['eventID'] = eventID

    def get_player(self, user: User):
        cantidates = [lply for lply in self.__players if lply.user.id == user.id]
        if not cantidates:
            return None
        return cantidates[0]
    def get_player_by_id(self, userID: int):
        cantidates = [lply for lply in self.__players if lply.user.id == userID]
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

    def __find_existing_game_such_as(self, user: User, form: GameCreationForm|dict):

        for lgame in self._gameLobby[form['gameMode']]:
            for lply in lgame.players:
                if not lgame.is_full and form == lgame.form:
                    return lgame
        return None

    def __find_player_in_lobby(self, user: User) -> LobbyGame|None:
        print('Trying __find_player_in_lobby with user : ', user.login)
        for gameMode, typedGames in self._gameLobby.items():
            for lgame in typedGames:
                for lply in lgame.players:
                    if user == lply.user:
                        print(f'Game containing user {user.login} FOUND ')
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
            return
            # raise MatchMakerException(f"Trying to remove game {lgame} from the lobby but this game does not exist in MatchMaker.")

        modeGames.remove(lgame)

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
            if (lgame.is_tournament and lgame.is_full) or lgame.is_live_tournament:
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

        print(f'MatchMaker :: connect_player :: Trying to connect user {user.login}. eventID: ', eventID)

        if eventID:
            finder_result = self.__find_event_in_lobby(user)
        else:
            finder_result = self.__find_player_in_lobby(user)
        #print('finder_result : ', finder_result)
        if not finder_result:
            return None
        gameMode, lgame, lply = finder_result
        lply.is_connected = True

        print('gameMode, gameType, lgame, lply: ', gameMode, lgame.gameType, lgame, lply)

        print(f'User {user.login} was SUCCESSFULLY connected !')
        return lgame

    def set_ready(self, user: User):
        finder_result = self.__find_player_in_lobby(user)
        if not finder_result:
            print('Player not in lobby while setting ready.')
            return None
        gameMode, lgame, lply = finder_result
        lply.is_ready = True
        return lgame



    def remove_player(self, user: User):
        print(f'\n MatchMaker :: remove_player :: removing user {user.login}')
        finder_result = self.__find_player_in_lobby(user)
        if not finder_result:
            return None
        print(f'MatchMaker :: remove_player :: FOUND USER')

        gameMode, lgame, lply = finder_result

        if lgame.nb_players == 1:
            print(f'MatchMaker :: remove_player :: last player gone. removing game from MatchMaker')
            self.remove_lobby_game(lgame)
        else:
            print(f'MatchMaker :: remove_player :: last player gone. removing player from lobby')
            lgame.remove_player(lply)

        if lgame.is_tournament or lgame.is_tournament_game:
            ''' If removing player from tournament init lobby or tournament game,
            try and cleanup both the tournament lobby and the game they are in. '''
            return self.remove_player(user)

        return (lgame, lply)

    def remove_player_from(self, user: User, lgame: LobbyGame):
        if not user in lgame:
            return
        lgame.remove_user(user)
        if lgame.is_empty:
            self.remove_lobby_game(lgame)

