from django.apps import AppConfig
import asyncio

class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'

    __match_maker = None#: MatchMaker # instanciated in ready()
    __game_gateway = None# instanciated in ready()

    @classmethod
    def __set_match_maker(cls, match_maker):
        cls.__match_maker = match_maker
    @classmethod
    def __set_game_gateway(cls, game_gateway):
        cls.__game_gateway = game_gateway

    @classmethod
    def get_match_maker(cls):
        return cls.__match_maker
    @classmethod
    def get_game_gateway(cls):
        return cls.__game_gateway
    
    @property
    def match_maker(self):
        return self.get_match_maker()
    @property
    def game_gateway(self):
        return self.get_game_gateway()

    def ready(self):
        from game.MatchMaker import MatchMaker
        from NetworkGateway.NetworkAdaptor import GameGateway
        from game.PingPongRebound.GameManager import GameManager#, testAllGames

        # messenger should be an instance of GameGateway, responsible
        # for providing message from the websocket to the GameManager 
        # and vice versa.
        GameConfig.__set_game_gateway(GameGateway())
        game_manager = GameManager(self.get_game_gateway())
        #asyncio.run(game_manager.addGame('Pong', 1))
        #asyncio.run(game_manager.startGame(1))
        #asyncio.run(asyncio.sleep(2))
        #asyncio.run(game_manager.removeGame(1))
        #testAllGames()
        GameConfig.__set_match_maker(MatchMaker(game_manager))
        #GameConfig.match_maker = MatchMaker(game_manager)
    #    print("GameConfig was just initialized !")
