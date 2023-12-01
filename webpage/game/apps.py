from django.apps import AppConfig
import asyncio

class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'

    __match_maker = None#: MatchMaker # instanciated in ready()

    @classmethod
    def __set_match_maker(cls, match_maker):
        cls.match_maker = match_maker

    @property
    def match_maker(self):
        return self.__match_maker

    def ready(self):
        from game.MatchMaker import MatchMaker
        from game.PingPongRebound.GameManager import GameManager#, testAllGames

        # messenger should be an instance of GameGateway, responsible
        # for providing message from the websocket to the GameManager 
        # and vice versa.
        fake_messenger = 1 
        game_manager = GameManager(fake_messenger)
        #asyncio.run(game_manager.addGame('Pong', 1))
        #asyncio.run(game_manager.startGame(1))
        #asyncio.run(asyncio.sleep(2))
        #asyncio.run(game_manager.removeGame(1))
        #testAllGames()
        GameConfig.__set_match_maker(MatchMaker(game_manager))
        #GameConfig.match_maker = MatchMaker(game_manager)
    #    print("GameConfig was just initialized !")
        pass