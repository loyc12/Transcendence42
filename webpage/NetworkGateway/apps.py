from django.apps import AppConfig


class NetworkgatewayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NetworkGateway'
    game_gateway = None

    @classmethod
    def __set_game_gateway(cls, gateway):
        game_gateway = gateway


    def ready(self):
        ''' Network Gatway initializer code. '''
        #from NetworkAdaptor import GameGateway
#
        #gateway = GameGateway()
        #self.__set_game_gateway(gateway)
        pass
