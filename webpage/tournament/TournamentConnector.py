from channels.layers import get_channel_layer
from tournament.models import Tournament
from NetworkGateway.consumers import GameConsumer
import asyncio
import json

class TournamentConnector:
    ''' Tournament connector holds the information necessary to handle the sending
        of Tournament updates.
    '''
    __channel_layer = get_channel_layer()
    __game_gateway = None # Set once by singleton GameGateway

    @classmethod
    def set_game_gateway(cls, game_gateway):
        if not cls.__game_gateway:
            cls.__game_gateway = game_gateway

    def __init__(self, initLobby):
        self.__tourDB: Tournament = None# Database instance returned when creating game instance in database.
        self.__player_consumers: dict[int, GameConsumer] = dict()
        self.__initLobby = initLobby
        self.__tour_lock = asyncio.Lock()

        self._is_closing = False



    @property
    def is_running(self):
        return self.__tourDB is not None
    @property
    def nb_connected(self):
        return len(self.__player_consumers)
    @property
    def tournament(self):
        return self.__tourDB
    @property
    def sockID(self):
        return self.__initLobby.tourID

    def set_tour_db_instance(self, tour: Tournament):
        if not (tour and isinstance(tour, Tournament)):
            raise TypeError('Trying to set tour instance to TournamentConnector, but object passed is not a Tournament model type.')
        self.__tourDB = tour


    async def connect_player(self, user, consumer):
        ''' Connects the player to the tournament socket. '''

        if user.id in self.__player_consumers:
            return

        async with self.__tour_lock:
            if user.id in self.__player_consumers:
                raise ValueError('Trying to add player to same tournament connector twice.')
            self.__player_consumers[user.id] = consumer

        await self.__channel_layer.group_add(
            self.sockID,
            consumer.channel_name
        )


    async def disconnect_player(self, user):
        print(f'GameConnector :: ENTER disconnect player')
        if not self.__initLobby:
            return None
        async with self.__tour_lock:
            if user.id not in self.__player_consumers:
                raise ValueError(f"Trying to disconnect user {user.login} from a game they don't belong to.")
            consumer = self.__player_consumers.pop(user.id)

        await self.__channel_layer.group_discard(self.sockID, consumer.channel_name)


    async def send_brackets(self, brackets_info):
        payload = json.dumps({
            'ev': 'brackets',
            'brackets': brackets_info
        })
        await self.__channel_layer.group_send(
            self.sockID,
            {
                'type': 'tour_send_brackets',
                'brackets': payload
            }
        )

    async def send_quitter_signal(self, quitterUser):
        if self._is_closing:
            return
        self._is_closing = True
        payload = json.dumps({
            'ev': 'quitter',
            'name': quitterUser.login,
            'img': quitterUser.img_link,
        })
        await self.__channel_layer.group_send(
            self.sockID,
            {
                'type': 'tour_send_quitter_signal',
                'signal': payload
            }
        )

    async def send_stage_initializer(self, lgame, stage):
        payload = json.dumps({
            'ev': 'game_connect',
            'sockID': lgame.sockID,
            'stage': str(stage),
            'form': lgame.form,
        })
        for lply in lgame.players:
            consumer = self.__player_consumers[lply.user.id]
            await consumer.send(text_data=payload)

    async def send_stage_initializer_to_finale_user(self, lgame, user):
        payload = json.dumps({
            'ev': 'game_connect',
            'sockID': lgame.sockID,
            'stage': 2,
            'form': lgame.form,
        })
        consumer = self.__player_consumers[user.id]
        await consumer.send(text_data=payload)