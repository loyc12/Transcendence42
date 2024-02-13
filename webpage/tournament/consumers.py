import sys
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async
from game.apps import GameConfig as app
import json

def eprint(*args):
    print(*args, file=sys.stderr)


class TournamentConsumerError(Exception):
    pass

class TournamentConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.sockID = self.scope['url_route']['kwargs']['sock_id']

        self.netGateway = app.get_game_gateway()
        if 'user' in self.scope:
            self.user = self.scope['user']
            self.userID = self.user.id
        else:
            raise TournamentConsumerError('A tournament tried to connect to a websocket without being logged in.')

        await self.accept()

        self.liveTour = await self.netGateway.connect_to_tournament(self.user, self)

    async def disconnect(self, event):
        eprint('TournamentConsumer :: disconnecting and wiping sessions data')
        self.netGateway.disconnect_tournament_member(self.user, self)

        raise StopConsumer

    async def receive(self, text_data):
        if not self.liveTour:
            raise TournamentConsumerError('TourConsumer :: Receiving data while no self.liveTour exists')
        event = json.loads(text_data)

        # Clean up input struct.
        event_type = event['ev']

        if event_type == 'final':
            await self.liveTour.join_final_game(self.user)

    async def tour_send_brackets(self, event):
        await self.send(text_data=event['brackets'])

    async def tour_send_quitter_signal(self, event):
        await self.send(text_data=event['signal'])
