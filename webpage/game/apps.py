from django.apps import AppConfig

class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'

    match_maker = None#: MatchMaker # instanciated in ready()

    def ready(self):
        from game.MatchMaker import MatchMaker
        from game.PingPongRebound import GameManager

        fake_messenger = 1
        game_manager = GameManager(fake_messenger)
        #importlib.import_module('game.MatchMaker')
        #importlib.import_module('game.PingPongRebound')

        GameConfig.match_maker = MatchMaker(game_manager)
    #    print("GameConfig was just initialized !")
        pass