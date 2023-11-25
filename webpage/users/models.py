from django.contrib.auth.models import AbstractBaseUser
from django.db import models, OperationalError, IntegrityError
#from django.utils import timezone
from .manager import UserManager

# class Session(models.Model):
#     session = models.CharField(primary_key=True, max_length=32, unique=True)
#     user = models.ForeignKey('login.User', on_delete=models.CASCADE)

class User(AbstractBaseUser):
    # Fields of table users_user
    login           = models.CharField    (primary_key=True, max_length=32, unique=True) #username
    display_name    = models.CharField    (max_length=60, unique=False) #full name
    img_link        = models.CharField    (max_length=120, unique=False) #profilePicture
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    is_active       = models.BooleanField (default=False) #status online/offline

    nb_games_played = models.PositiveIntegerField(default=0)
    wins            = models.PositiveIntegerField(default=0)
    loses           = models.PositiveIntegerField(default=0)
    
    #session_link
    # session         = models.ForeignKey('sessions.Session', on_delete=models.CASCADE)
    
    #Ze thing
    # class Meta:
    #     unique_together = ('login','session')

    USERNAME_FIELD = "login"
    
    # Method that return a string with the information of the user
    objects = UserManager()

    def __str__(self):
        return f"User: {self.login},\
                display_name: {self.display_name},\
                created_at: {self.created_at},\
                updated_at: {self.updated_at}"

    @property
    def current_game(self):
        cur_games = self.game_set.get(is_running=True)
        if not cur_games:
            return None
        elif cur_games.count() > 1:
            raise IntegrityError('User should not be referenced in multiple running games.')
        else:
            return cur_games.first()
        
    @property
    def is_ingame(self):
        return (self.current_game is not None)
    
    @property
    def nb_games_played(self):
        games_played = self.player_set.get(user=self.id)
        return games_played.count()

    def update_stats(self, save: bool=True):
        games_played = self.player_set.get(user=self.id)
        nb_games_played = games_played.count()
        nb_wins = self.game_set.get(winner=self.id).count()
        nb_loses = nb_games_played - nb_wins
        print("nb_games_played : ", nb_games_played)

        self.nb_games_played =  nb_games_played
        self.nb_wins =          nb_wins
        self.nb_loses =         nb_loses

        # ...

        if save:
            self.save()
        

    # def leave_game(self, save: bool):
    #     cur_game = self.current_game
    #     if not cur_game:
    #         return
    #     cur_game.declare_broken()
    #     #self.current_game = None
    #     if save:
    #         self.save()

    def join_game(self, game):
        #if not game.can_join(self):
        #    raise OperationalError('Trying to join game while already playing in another.') 
        cur_game = self.current_game
        if cur_game == game:
            return
        if cur_game and cur_game != game:
            raise OperationalError('User trying to join game while already member of another.')
            
        #self.current_game = game
        game.add_player(self)
        self.save()


