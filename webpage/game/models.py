import sys
import hashlib
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError, OperationalError
from users.models import User
from asgiref.sync import sync_to_async


def eprint(*args):
    print(*args, file=sys.stderr)

# Create your models here.
class Player(models.Model):
    user =          models.ForeignKey(User, on_delete=models.CASCADE)
    game =          models.ForeignKey('Game', on_delete=models.CASCADE)
    joined_at =     models.DateTimeField(auto_now_add=True)
    score =         models.IntegerField(default=0)
    gave_up =       models.BooleanField(default=False)
    #default_win =   models.BooleanField(default=False)

class Game(models.Model):

    game_type =     models.CharField(max_length=16, default='Pong')
    max_players =   models.IntegerField(default=2)
    created_at =    models.DateTimeField(auto_now_add=True)
    started_at =    models.DateTimeField(null=True, blank=True, default=None)
    ended_at =      models.DateTimeField(null=True, blank=True, default=None)
    players =       models.ManyToManyField('users.User', through=Player)# should be ordered according to joined_at parameter of Player model.

    is_official =   models.BooleanField(default=False)
    is_running =    models.BooleanField(default=False)
    is_over =       models.BooleanField(default=False)
    is_broken =     models.BooleanField(default=False)
    is_abandoned =  models.BooleanField(default=False)

    winner =        models.ForeignKey('users.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='game_winner')
    finale_scores = models.JSONField(max_length=150, default=dict)


    def __str__(self):
        return f"<--------Game id {str(self.id)}--------->" +\
                f"\n<-| game type :     {self.game_type}" +\
                f"\n<-| nb players :    {self.max_players}" +\
                f"\n<-| is running :    {self.is_running}" +\
                f"\n<-| is over :       {self.is_over}" +\
                f"\n<-| winner :        {self.winner.login if self.winner else 'None'}" +\
                f"\n<-| final score :   {self.finale_scores if self.finale_scores else 'None'}" +\
                "\n<---------------------------------->"

    def __repr__(self):
        return (self.__str__())

    def get_apiID(self) -> str:
        return hashlib.sha256(f'{self.id};{self.created_at};{self.game_type}'.encode()).hexdigest()

    @property
    def apiKey(self):
        return self.get_apiID()

    @classmethod
    def force_stop_all_games(cls):
        running_games = Game.objects.filter(is_running=True)
        for game in running_games:
            game.declare_broken()


    @property
    def ready_to_start(self) -> bool:
        return (
            not self.is_running
            and not (self.is_over or self.is_broken)
            and self.players.count() == self.max_players
        )

    @property
    def is_full(self):
        return self.players.count() == self.max_players

    def can_join(self, user: User) -> bool:
        return (
            not (
                self.is_running or self.is_over or self.is_broken
                or self.is_full or user.current_game
            )
        )

    def add_player(self, user: User, save: bool=True):

        if self.is_running or self.is_over or self.is_broken:
            raise OperationalError('Trying to join a live game or an already finished game or a broken game.')

        cur_game = user.current_game
        if cur_game:
            if cur_game != self:
                raise OperationalError('Trying to add player when they are already in a different game.')
            return

        if self.is_full:
            raise OperationalError('Trying to add player when the game is already full.')

        self.players.add(user)

        if save:
            self.save()


    def declare_broken(self, save: bool=True) -> None:
        if self.is_over:
            raise OperationalError('Cannot declare a game broken after its already over.')

        self.timestamp_end()
        self.is_running = False
        self.is_over = True
        self.is_broken = True
        if save:
            self.save()

    def declare_started(self, save: bool=True) -> None:
        if self.is_over or self.is_broken:
            raise OperationalError('Cannot start a game that is already over or broken.')

        self.timestamp_start()
        self.is_running = True
        if save:
            self.save()

    def timestamp_start(self):
        self.started_at = datetime.now()
    def timestamp_end(self):
        self.ended_at = datetime.now()

    @sync_to_async
    def stop_and_register_results(self, scores: dict[int, int], quitter=0):
        '''
            Sets the game as over.
            params:
                - scores: should have len == max_players for the game type
                and be a dict with player id as key and score as value.
        '''
        eprint('Game DB model :: CALLED stop_and_register_results')
        eprint('Game DB model :: scores : ', scores)
        eprint('Game DB model :: scores type : ', type(scores))
        if len(scores) != self.max_players:
            raise OperationalError(f"Wrong nb of player scores ({len(scores)}) in scores dict.")
        if not self.is_running:
            raise OperationalError("Trying to register results and end a game, when the game hasn't started yet.")

        plys = Player.objects.filter(game=self)
        eprint('Game DB model :: players : ', plys)

        if self.is_official:
            # Set score for individual players in game
            for ply, s in zip(plys, scores):
                ply.score = s
                eprint(f'Player ({ply.user.login}) score set to {ply.score} in game {self.id}')

            if quitter > 0:
                for ply in plys:
                    if ply.user.id == quitter:
                        break
                if ply.user.id == quitter:
                    ply.gave_up = True

                self.is_abandoned = True

            elif plys.count() > 1:
                # Find winner
                eprint('Trying to set game winner in DB')
                # o_plys = plys.order_by('-score')
                winner = plys[scores.index(max(scores))]
                self.winner = winner.user  #o_plys.first().user
                eprint(f'game id {self.id} Winner set as : ', self.winner)

            plys.bulk_update(plys, ['score', 'gave_up'])
#

        # Set end of game state
        self.is_running = False
        self.is_over = True

        self.timestamp_end()
        self.finale_scores = scores
        self.save()
        return ('wow')

    @sync_to_async
    def stop_and_register_force_close(self):
        self.declare_broken(save=True)