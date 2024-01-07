import sys
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async
from game.apps import GameConfig as app
import json
# from game.MatchMaker import LobbyGame
# import asyncio

def eprint(*args):
    print(*args, file=sys.stderr)


class TournamentConsumerError(Exception):
    pass
# class TournamentConsumerWarning(Warning):
#     pass

class TournamentConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.sockID = self.scope['url_route']['kwargs']['sock_id']
        print('tournament :::::: CONNECTING TO WEBSOCKET with id : ', self.sockID)

        self.netGateway = app.get_game_gateway()
        if 'user' in self.scope:
            print('scope DOES contain user. ')
            self.user = self.scope['user']
            self.userID = self.user.id
            print(self.user)
            print('user id : ', self.user.id)
        else:
            raise TournamentConsumerError('A tournament tried to connect to a websocket without being logged in.')

        await self.accept()

        self.liveTour = await self.netGateway.connect_to_tournament(self.user, self)

        # await self.send(text_data=json.dumps({
        #     'ev': 'connect',
        #     'msg': 'Hello there buddy !'
        # }))


    async def disconnect(self, event):
        # session_data = self.scope['session']
        # session_data.pop("tournament_id")
        # session_data.pop("tournament_login")
        # session_data.save()
        print('\n\ntournament Websocket disconnecting !\n\n')
        eprint('TournamentConsumer :: disconnecting and wipping sessions data')
        # session_data.delete()
        # #Save deletes the session data and the session key, and it deletes the session from the database.
        # session_data.save()
        eprint('TournamentConsumer :: closing tournament websocket')
        # self.tournament.is_active = False
        # await sync_to_async(self.tournament.save)()
        self.netGateway.disconnect_tournament_member(self.user, self)

        raise StopConsumer
    # async def tour_new_connection_message(self, event):
    #     await self.send(text_data=event['brackets'])

    async def receive(self, text_data):
        if not self.liveTour:
            raise TournamentConsumerError('TourConsumer :: Receiving data while no self.liveTour exists')
        event = json.loads(text_data)

        # Clean up input struct.
        event_type = event['ev']

        if event_type == 'final':
            await self.liveTour.join_final_game(self.user)
            # await self.liveTour.connector.send_brackets(self.liveTour.get_brackets_info())



    async def tour_send_brackets(self, event):
        print('TournamentConsumer :: tour_send_brackets entered' )
        await self.send(text_data=event['brackets'])

    async def tour_send_quitter_signal(self, event):
        print('TournamentConsumer :: tour_send_quitter_signal entered' )
        print("event['signal'] : ", event['signal'])
        await self.send(text_data=event['signal'])



    # async def tour_send_stage_connection_msg(self, lgame):
    #     payload = json.dumps({
    #         'ev': 'game_connect',
    #         'sockID': lgame.sockID
    #     })
    #     self.group_send(
    #         lgame.
    #     )
