import sys
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, OperationalError, IntegrityError
from game.MatchMaker import LobbyGame
from asgiref.sync import sync_to_async


def eprint(*args):
    print(*args, file=sys.stderr)

# Create your models here.
class TourMember(models.Model):
    user =          models.ForeignKey('users.User', on_delete=models.CASCADE)
    Tournament =    models.ForeignKey('Tournament', on_delete=models.CASCADE)
    joined_at =     models.DateTimeField(auto_now_add=True)
    gave_up =       models.BooleanField(default=False)

class Tournament(models.Model):
    # Fields of table Tournaments_Tournament
    id              = models.AutoField    (primary_key=True)
    max_players     = models.IntegerField (default=4)
    group_size      = models.IntegerField (default=2)

    members         = models.ManyToManyField('users.User', through=TourMember)

    groupAGame      = models.ForeignKey   ('game.Game', on_delete=models.CASCADE, related_name='groupAGame', null=True, blank=True)#Round1
    groupBGame      = models.ForeignKey   ('game.Game', on_delete=models.CASCADE, related_name='groupBGame', null=True, blank=True)#Round1
    groupCGame      = models.ForeignKey   ('game.Game', on_delete=models.CASCADE, related_name='groupCGame', null=True, blank=True)#Round2

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    winner          = models.ForeignKey   ('users.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='tour_winner')

    is_over         = models.BooleanField (default=False)
    is_running      = models.BooleanField (default=False)
    is_broken       = models.BooleanField (default=False)
    is_abandoned    = models.BooleanField (default=False)

    def __str__(self):
        return f"Tournament {self.id} : {self.max_players} players, {self.group_size} players per group."


    @property
    def current_tournament(self):
        try:
            cur_tournaments = self.tournament_set.filter(is_active=True)
        except ObjectDoesNotExist:
            return None

        if cur_tournaments.count() > 1:
            raise IntegrityError('Tournament should not be referenced in multiple running tournaments.')
        else:
            return cur_tournaments.first()

    @property
    def is_full(self):
        eprint('Tournament model :: self.members : ', self.members)
        eprint('Tournament model :: self.members.count() : ', self.members.count())
        return self.members.count() == 4

    @sync_to_async
    def addGroupAGame(self, game: LobbyGame):
        self.groupAGame = game.game_connector.game
        self.save()

    @sync_to_async
    def addGroupBGame(self, game: LobbyGame):
        self.groupBGame = game.game_connector.game
        self.save()

    @sync_to_async
    def addGroupCGame(self, game: LobbyGame):
        self.groupCGame = game.game_connector.game
        self.save()

    @sync_to_async
    def declare_started(self):
        self.is_running = True
        self.is_broken = False
        self.is_over = False
        self.save()

    @sync_to_async
    def declare_broken(self):
        self.is_running = False
        self.is_broken = True
        self.is_over = True
        self.save()

    @sync_to_async
    def declare_abandoned(self):
        self.is_running = False
        self.is_broken = True
        self.is_abandoned = True
        self.is_over = True
        self.save()

    @sync_to_async
    def declare_over(self):
        self.is_running = False
        self.is_over = True
        self.save()

    @sync_to_async
    def force_shutdown(self, is_abandoned=False):
        if is_abandoned:
            self.declare_abandoned()
        else:
            self.declare_broken()
        self.save()


    @sync_to_async
    def add_member(self, user, save: bool=True):

        if self.is_running or self.is_over or self.is_broken:
            raise OperationalError('Trying to join a live game or an already finished game or a broken game.')

        cur_game = user.current_game
        if cur_game:
            if cur_game != self:
                raise OperationalError('Trying to add player when they are already in a different game.')
            return

        if self.is_full:
            raise OperationalError('Trying to add player when the game is already full.')

        self.members.add(user)

        if save:
            self.save()

    def join_tournament(self, tournament):
        cur_tournament = self.current_tournament
        if cur_tournament == tournament:
            return
        if cur_tournament and cur_tournament != tournament:
            raise OperationalError('Tournament trying to join tournament while already member of another.')

        tournament.add_player(self)
        self.save()


