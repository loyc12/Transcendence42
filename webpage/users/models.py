from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin 
from django.db import models, OperationalError, IntegrityError
#from django.utils import timezone
from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    # Fields of table users_user
    login           = models.CharField    (max_length=32, unique=True)
    display_name    = models.CharField    (max_length=60, unique=False)
    img_link        = models.CharField    (max_length=120, unique=False) 
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    is_active       = models.BooleanField (default=False)
    socket_id       = models.CharField    (max_length=120, unique=False)
    #running_game =  models.CharField(max_length=32, default='')
    #running_game =  models.CharField(max_length=32, default='')
    #current_game =  models.ForeignKey('game.Game', on_delete=models.SET_NULL, null=True, default=None)
    # Variable that contain the name of the field used to identify the user
    USERNAME_FIELD = "login"
    
    # Method that return a string with the information of the user
    objects = UserManager()

    def __str__(self):
        return f"User: {self.login},\
                display_name: {self.display_name},\
                created_at: {self.created_at},\
                updated_at: {self.updated_at}"
                
'''
# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

    # DB Fields
    email =         models.EmailField(unique=True)
    username =      models.CharField(max_length=32, unique=False)
    created_at =    models.DateTimeField(auto_now_add=True)
    updated_at =    models.DateTimeField(auto_now=True)
    is_staff =      models.BooleanField(default=False)
    is_superuser =  models.BooleanField(default=False)
    is_active =     models.BooleanField(default=False)
    #running_game =  models.CharField(max_length=32, default='')
    #running_game =  models.CharField(max_length=32, default='')
    #current_game =  models.ForeignKey('game.Game', on_delete=models.SET_NULL, null=True, default=None)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"User: {self.username}, email: {self.email}, created_at: {self.created_at}, updated_at: {self.updated_at}, hash: {self.password}"
'''


@property
def current_game(self):
    cur_games = self.game_set.get(is_running=True)
    if not cur_games:
        return None
    elif cur_games.count() > 1:
         raise IntegrityError('User should not be referenced in multiple running games.')
    else:
           return cur_games.first()
#Game.objects.get(is_running=True)

def leave_game(self, save: bool):
    cur_game = self.current_game
    if not cur_game:
        return
    self.current_game.declare_broken()
    #self.current_game = None
    if save:
      self.save()

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


