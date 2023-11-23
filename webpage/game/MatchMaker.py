from users.models import User
from game.models import Game
from game.forms import GameCreationForm
from game.PingPongRebound import Pong, Ponger, Pongest, Pongester, Ping, Pinger, Pingest

''' We can assume this msg struct is correct since the frontend UI
can only propose valid choices. '''
test_join_msg = {
    'game_mode': 'Freeplay',
    'game_type': 'Pong'
}

class MatchMakerException(Exception):
    pass

class MatchMaker:
    
    def __init__(self):

        self._gameLobby = {
            'Tournament': [],
            'Freeplay': [],
            'Local_1p': [],
            'Local_2p': []
        }

    def __find_existing_game_such_as(game_mode: str, form: GameCreationForm|dict):
    
        for t in self._gameLobby[game_mode]:
            if form == t[0]:
                return t
        return None


    def join_lobby(self, user: User, form: GameCreationForm|dict):
        ''' Can accept either GameCreationForm.cleaned_data objects or 
        popperly formated dict with valid entries for "game_mode" and "game_type". 
        Then, if valid, instanciates the game in the database and puts  '''

        game_mode = form.get('game_mode')
        game_type = form.get('game_type')
        if not game_mode or not game_type:
            raise ValueError('Missing one or more fields in form.')

        sim_game = self.__find_existing_game_such_as(form)
        if sim_game:
            if user in sim_game[1]:
                raise MatchMakerException(f'User {user.username} tried to join a game twice. Stop that !')

            ### TODO: check that the game isn't full before adding.
            sim_game[1].add(user)
        else
            self.gameLobby[game_mode].append((form, {user}))
            
