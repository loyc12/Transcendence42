from dataclasses import dataclass
from users.models import User
from game.models import Game
from game.forms import GameCreationForm
#from game.PingPongRebound import Pong, Ponger, Pongest, Pongester, Ping, Pinger, Pingest
#from game.PingPongRebound import GameManager as gm#Po, Pi, Pong, Ping, Ponger, Pinger, Pongest, Pingest
#from game.PingPongRebound import GameManager
import asyncio

''' We can assume this msg struct is correct since the frontend UI
can only propose valid choices. '''
test_join_msg = {
    'gameMode': 'Freeplay',
    'gameType': 'Pong'
}

class MatchMakerException(Exception):
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

    @classmethod
    def __get_lobby_id(cls):
        cls.__id_counter += 1
        return cls.__id_counter

    def __init__(self, form: GameCreationForm, players: list[LobbyPlayer]):
        self.__id: int = self.__get_lobby_id()
        self.form: GameCreationForm = form
        self.players: list[LobbyPlayer] = list()

    @property
    def lobbyID(self):
        return self.__id
    @property
    def sockID(self):
        return "sock{:.06d}".format(self.__id)
    
    @property
    def players(self):
        return [lply.user.display_name for lply in self.players]


class MatchMaker:

    _maxRacketCounts = dict()
    
    
    def __init__(self, game_manager = None):

        self.gm = game_manager

        self._gameLobby = {
            'Tournament': [],
            'Multiplayer': [],
            'Local_1p': [],
            'Local_2p': []
        }

        if not MatchMaker._maxRacketCounts:
            MatchMaker._maxRacketCounts['Pong'] = self.gm.getMaxPlayerCount('Pong')
            MatchMaker._maxRacketCounts['Ping'] = self.gm.getMaxPlayerCount('Ping')
            MatchMaker._maxRacketCounts['Pingest'] = self.gm.getMaxPlayerCount('Pingest')
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


    def has_game(self, gameID):
        pass
    def has_player(self, user: User):
        pass


    def is_game_full(self, gameType: str, lgame: LobbyGame):
        return len(lgame.players) == self._maxRacketCounts[gameType]

    def is_game_ready(self, gameType: str, lgame: LobbyGame):
        return self.is_game_full(gameType, lgame)\
            and all(lply.is_connected for lply in lgame.players)


    def __find_existing_game_such_as(self, user: User, form: GameCreationForm|dict):
    
        for lgame in self._gameLobby[form['gameMode']]:
            for lply in lgame.players:
                if user == lply.user:
                    raise MatchMakerException(f'User {user.username} tried to join a game twice. Stop that !')
                if not self.is_game_full(form['gameType'], lgame) and form == lgame.form:
                    return lgame
        return None

    def __find_player_in_lobby(self, user: User) -> LobbyGame|None:
        for gameType, lgame in self._gameLobby.items():
            for lply in lgame.players:
                if user == lply.user:
                    return (gameType, lgame, lply)
        return None


    def __remove_lobby_game(self, lgame: LobbyGame):
        game_type = lgame.form.get('gameType')
        if not game_type or not game_type in self._gameLobby:
            raise MatchMakerException(f"Trying to remove game {lgame} from the lobby but the game's gameType does not exist.")
        self._gameLobby[game_type].remove(lgame)

    async def __push_game_to_gamemanager(self, gameType: str, lgame: LobbyGame):
        ''' When calling this function, the game should be validated ready to start. '''
        game = Game.objects.create(
            game_type=gameType,
            max_players=self._maxRacketCounts[gameType]
        )
        gm_status = await self.gm.addGame(gameType, game.id)
        if not gm_status:
            raise MatchMakerException('Error occured while trying to create new game in game_manager.')

        for lply in lgame.players:
            game.add_player(lply.user)
            await self.gm.addPlayerToGame(lply.user.id, lply.user.login, game.id)
        
        self.__remove_lobby_game(lgame)
        game.declare_started()


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
        if lgame:
            if self.is_game_full(gameType, lgame):
                raise MatchMakerException('User trying to join a game that is already full.')

            # Game should be fully validated at this point
            lply = LobbyPlayer(user=user, is_connected=False)
            lgame.players.append(lply)
        else:
            lply = LobbyPlayer(user=user, is_connected=False, is_ready=False)
            lgame = LobbyGame(form=form, players=[lply])
            self._gameLobby[gameMode].append(lgame)
            print("Match Maker Game Lobby : ", self._gameLobby)

        return lgame


    def connect_player(self, user: User):
        ''' Called by websocked when player connects to the games websocker with lobbyID
            after having called join_lobby() first, but before the game has officialy 
            been created. '''
        finder_result = self.__find_player_in_lobby(user)
        if not finder_result:
            return False
        gameType, lgame, lply = finder_result
        lply.is_connected = True
        
        # TODO : Return lgame.players list of names and connected status to user
        # through websocket.
        if self.is_game_full(gameType, lgame):
            asyncio.run(self.__push_game_to_gamemanager(gameType, lgame))
        return lgame

        

    def remove_player(self, user: User):
        #gameType, lgame, lply = self.__find_player_in_lobby(user)
        finder_result = self.__find_player_in_lobby(user)
        if not finder_result:
            return False
        
        gameType, lgame, lply = finder_result
        if len(lgame.players) == 1:
            self._maxRacketCounts[gameType].remove(lgame)
        else:
            lgame.players.remove(lply)

        return True

