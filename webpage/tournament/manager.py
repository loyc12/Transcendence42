
#class TournamentManager(TournamentManager):#(BaseTournamentManager):
class TournamentManager:
# Class object containing the methods to: create a tournament,
    def create_tournament(self, login, **extra_fields):
        tournament = self.model(login=login, **extra_fields)
        tournament.save()
        return tournament
