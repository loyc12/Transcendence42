from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin 
from django.db import models, OperationalError
#from django.utils import timezone
from .manager import UserManager
#from game.models import Game

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
    current_game =  models.ForeignKey('game.Game', on_delete=models.SET_NULL, null=True, default=None)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"User: {self.username}, email: {self.email}, created_at: {self.created_at}, updated_at: {self.updated_at}, hash: {self.password}"
    
    def leave_game(self, save: bool):
        if not self.current_game:
            return
        
        if self.current_game.is_running:
            self.current_game.declare_broken()
        self.current_game = None
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
        
        self.current_game = game
        game.add_player(self)
        self.save()


