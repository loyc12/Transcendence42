import sys
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async
#import asyncio
import json


def eprint(*args):
    print(*args, file=sys.stderr)

class TournamentConsumerError(Exception):
    pass
class TournamentConsumerWarning(Warning):
    pass

class TournamentConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.sockID = self.scope['url_route']['kwargs']['sock_id']
        print('tournament :::::: CONNECTING TO WEBSOCKET with id : ', self.sockID)

        if 'tournament' in self.scope:
            print('scope DOES contain tournament. ')
            self.tournament = self.scope['tournament']
            self.tournamentID = self.tournament.id
            print(self.tournament)
            print('tournament id : ', self.tournament.id)
        else:
            raise TournamentConsumerError('A tournament tried to connect to a websocket without being logged in.')
        await self.accept()
        await self.send(text_data=json.dumps({
            'ev': 'connect',
            'msg': 'Hello there buddy !'
        }))


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
        self.tournament.is_active = False
        await sync_to_async(self.tournament.save)()
        raise StopConsumer