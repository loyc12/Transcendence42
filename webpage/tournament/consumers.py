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
        raise StopConsumer

    # async def tour_new_connection_message(self, event):
    #     await self.send(text_data=event['brackets'])

    async def tour_send_brackets(self, event):
        await self.send(text_data=event['brackets'])


    # async def tour_send_stage_connection_msg(self, lgame):
    #     payload = json.dumps({
    #         'ev': 'game_connect',
    #         'sockID': lgame.sock_id
    #     })
    #     self.group_send(
    #         lgame.
    #     )
