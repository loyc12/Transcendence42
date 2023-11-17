from django.db import models, IntegrityError, OperationalError
from users.models import User
from datetime import datetime


# Create your models here.
class Player(models.Model):
    user =          models.ForeignKey(User, on_delete=models.CASCADE)
    game =          models.ForeignKey('Game', on_delete=models.CASCADE)
    joined_at =     models.DateTimeField(auto_now_add=True)
    score =         models.IntegerField(default=0)

class Game(models.Model):

    #group_id =      models.CharField(primary_key=True, max_length=16, unique=True, )# same as websocket channel group.
    game_type =     models.CharField(max_length=16, default='Pong')
    max_players =   models.IntegerField(default=2)
    created_at =    models.DateTimeField(auto_now_add=True)
    ended_at =      models.DateTimeField(null=True, blank=True, default=None)
    host =          models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='game_host')
    players =       models.ManyToManyField(User, through=Player)# should be ordered according to joined_at parameter of Player model.

    is_running =    models.BooleanField(default=False)
    is_over =       models.BooleanField(default=False)
    is_tournament = models.BooleanField(default=False)
    is_broken =     models.BooleanField(default=False)

    winner =        models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='game_winner')
    #finale_scores = models.CharField(max_length=32)# scores in string, separated by ';' : "<player1>;<player2>;...;<playerN>"
    finale_scores = models.JSONField(null=True, blank=True, max_length=100)


    def __str__(self):
        return f"<--------Game id {str(self.id)}--------->" +\
                "\n<-| game type :     " + self.game_type +\
                "\n<-| nb players :    " + str(self.max_players) +\
                "\n<-| host :          " + (self.host.username if self.host else 'None') +\
                "\n<-| is running :    " + str(self.is_running) +\
                "\n<-| is over :       " + str(self.is_over) +\
                "\n<-| is tournament : " + str(self.is_tournament) +\
                "\n<-| winner :        " + (self.winner.username if self.winner else 'None') +\
                "\n<-| final score :   " + (self.finale_scores if self.finale_scores else 'None') +\
                "\n<---------------------------------->"
    
    def __repr__(self):
        return (self.__str__())

    @property
    def ready_to_start(self) -> bool:
        return (
            not self.is_running
            and not self.is_over
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

    def add_player(self, user: User):

        if self.is_running or self.is_over or self.is_broken:
            raise OperationalError('Trying to join a live game or an already finished game or a broken game.')

        if user.current_game:
            if user.current_game != self:
                raise OperationalError('Trying to add player when they are already in a different game.')
            return

        if self.is_full:
            raise OperationalError('Trying to add player when the game is already full.')

        #if nb_players == 0;
        #    self.host = user
        user.join_game(self)
        self.players.add(user)
        self.save()

        if self.ready_to_start:
            pass


    def declare_broken(self) -> None:
        if self.is_over:
            raise OperationalError('Cannot declare a game broken after its already over.')

        self.ended_at = datetime.now()
        self.is_running = False
        self.is_over = True
        self.is_broken = True


    def __flush_all_players(self):
        ''' Removes this game from each player's current_game variable back to NULL.
         Does NOT remove the users from the game's players field since it is used to log
         the games data long term for users to track their stats through games they played in.
         This will allow players to join an other game in the future. This should only
         be done when the it is time to cut ties with between the game and its players 
         to definitly in at runtime. '''
        
        plys = self.players.all()
        for ply in plys:
            ply.leave_game(save=False)
        User.objects.bulk_update(plys, ['current_game'])# batch updates to postgres rather then individual saves.



    def stop_and_register_results(self, scores: dict[int, int]):
        ''' 
            Sets the game as over.
            params:
                - scores: should have len == max_players for the game type
                and be a dict with player id as key and score as value.
        '''
        if not isinstance(scores, dict):
            raise TypeError('scores param must be a dict.')
        if len(scores) != self.max_players:
            raise OperationalError(f"Wrong nb of player scores ({len(scores)}) in scores dict.")
        if not self.is_running:
            raise OperationalError("Trying to register results and end a game, when the game hasn't started yet.")

        plys = Player.objects.filter(game=self)
        if len(plys) != self.max_players:
            raise IntegrityError("Nb of players registered to the game does not fit the number required for this game type.")
        
        # Set score for individual players in game
        for ply in plys:
            ply.score = scores[ply.user.id]
        plys.bulk_update(plys, ['score'])# batch updates to postgres rather then individual saves.

        # Find winner
        o_plys = plys.order_by('-score')
        self.winner = o_plys.first()

        # Set end of game state
        self.is_running = False
        self.is_over = True
        self.ended_at = datetime.now()

        self.finale_scores = scores
        
        self.__flush_all_players()
        self.save()
