import hashlib
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, OperationalError, IntegrityError
#from django.utils import timezone
from asgiref.sync import sync_to_async

from .manager import UserManager


class User(AbstractBaseUser):
    # Fields of table users_user
    login           = models.CharField    (max_length=32, unique=True) #username
    display_name    = models.CharField    (max_length=60, unique=False) #full name
    img_link        = models.CharField    (max_length=120, unique=False) #profilePicture
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    is_active       = models.BooleanField (default=False) #status online/offline

    USERNAME_FIELD = "login"

    # Method that return a string with the information of the user
    objects = UserManager()

    @classmethod
    @sync_to_async
    def get_user(cls, userID: int):
        try:        user = cls.objects.get(id=userID)
        except ObjectDoesNotExist: return None
        return user

    def __str__(self):
        return f"User: {self.login},\
                display_name: {self.display_name},\
                created_at: {self.created_at},\
                updated_at: {self.updated_at}"

    def get_apiID(self) -> str:
        return hashlib.sha256(f'{self.id};{self.login};{self.created_at};{self.last_login}'.encode()).hexdigest()

    @property
    def apiKey(self):
        return self.get_apiID()

    @property
    def current_game(self):
        try:
            cur_games = self.game_set.filter(is_running=True)
        except ObjectDoesNotExist:
            return None
        if cur_games.count() > 1:
            raise IntegrityError('User should not be referenced in multiple running games.')
        else:
            return cur_games.first()

    @property
    def is_ingame(self):
        return (self.current_game is not None)

    @property
    def nb_games_played(self):
        try:    return self.player_set.filter(user=self.id).count()
        except ObjectDoesNotExist: return 0

    @property
    def nb_official_games_played(self):
        try:    return self.player_set.filter(user=self.id, game__is_official=True).count()
        except ObjectDoesNotExist: return 0

    @property
    def nb_official_games_finished(self):
        try:    return self.player_set.filter(user=self.id, game__is_official=True, game__is_abandoned=False, game__is_over=True).count()
        except ObjectDoesNotExist: return 0

    @property
    def nb_wins(self):
        try:    return self.game_set.filter(winner=self.id, is_official=True).count()
        except ObjectDoesNotExist: return 0

    @property
    def nb_losses(self):
        try:    return self.player_set.filter(user=self.id, game__is_official=True, game__is_abandoned=False).exclude(game__winner=self.id).count()
        except ObjectDoesNotExist: return 0

    @property
    def nb_given_up(self):
        try:    return self.player_set.filter(user=self.id, game__is_official=True, gave_up=True).count()
        except ObjectDoesNotExist: return 0

    @property
    def nb_rug_pulled(self):
        try:    return self.player_set.filter(user=self.id, game__is_official=True, game__is_abandoned=True, gave_up=False).count()
        except ObjectDoesNotExist: return 0

    @property
    def win_loss_ratio(self):
        nb_played = self.nb_official_games_finished
        nb_wins = self.nb_wins
        if nb_wins == 0:
            return 0
        if nb_played == nb_wins:
            return 1.0
        return nb_wins / nb_played
    
    @property
    def nb_tournaments_won(self):
        try:    return self.tournament_set.filter(winner=self.id).count()
        except ObjectDoesNotExist: return 0

    def join_game(self, game):
        cur_game = self.current_game
        if cur_game == game:
            return
        if cur_game and cur_game != game:
            raise OperationalError('User trying to join game while already member of another.')

        game.add_player(self)
        self.save()


