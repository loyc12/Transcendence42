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
        # self.__sockID: str = sockID
        self.__tourDB: Tournament = None# Database instance returned when creating game instance in database.
        self.__player_consumers: dict[int, GameConsumer] = dict()
        self.__initLobby = initLobby
        self.__tour_lock = asyncio.Lock()
        print('Creating TournamentConnector :: with sockID : ', self.sockID)

        # self.lobby_game = None # Returned after connecting to MatchMaker


    @property
    def is_running(self):
        return self.__tourDB is not None
    @property
    def nb_connected(self):
        return len(self.__player_consumers)
    #@property
    #def match_maker(self):
    #    return self.__game_gateway.match_maker
    @property
    def tournament(self):
        return self.__tourDB
    # @property
    # def tourID(self):
    #     return self.__tourDB.id
    @property
    def sockID(self):
        return self.__initLobby.tourID
        # return self.__sockID

   # def set_lobby_game(self, lgame):
   #     if self.lobby_game and lgame != self.lobby_game:
   #         GameGatwayException('Trying to set game_connector.lobby_game to different game. lobby_game can only be set once.')
   #     self.lobby_game = lgame

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
        # asyncio.gather(
        # await self.send_brackets()
        # )


    async def disconnect_player(self, user):
        print(f'GameConnector :: ENTER disconnect player')
        if not self.__initLobby:
            return None
        async with self.__tour_lock:
            if user.id not in self.__player_consumers:
                raise ValueError(f"Trying to disconnect user {user.login} from a game they don't belong to.")
            consumer = self.__player_consumers.pop(user.id)

        #await self.send_end_state(end_state);

        ### TODO: Manage early exit from tournament.

        await self.__channel_layer.group_discard(self.sockID, consumer.channel_name)

        # print(f'TournamentConnector :: SWITCH')
        # if self.game:
        #     ## TODO: Disconnect player while in live game.
        #     print(f'TournamentConnector :: disconnect player {user.id} INGAME')
        #     await self.push_event(user.id, 'end_game') # send disconnect event to Game instance in game manager. Same place as keypress events.

        # elif self.nb_connected > 0:
        #     print(f'TournamentConnector :: disconnect player {user.id} while IN LOBBY')
        #     await self._send_players_list()
        # else:
        #     print('WTF DUDE !!')


    async def send_brackets(self, brackets_info):
        print('TournamentConnector :: end_brackets() entered')
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

    async def send_stage_initializer(self, lgame, stage):
        print(f'TCONN :: send_stage_initializer starting game {lgame.sockID}')
        payload = json.dumps({
            'ev': 'game_connect',
            'sockID': lgame.sockID,
            'stage': stage,
            'form': lgame.form,
        })
        for lply in lgame.players:
            consumer = self.__player_consumers[lply.user.id]
            await consumer.send(text_data=payload)

        # await self.__channel_layer.group_send(
        #     self.sockID,
        #     {
        #         'type': 'tour_new_connection_message',
        #         'brackets': payload
        #     }
        # )
