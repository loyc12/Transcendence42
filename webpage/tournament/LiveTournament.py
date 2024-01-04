import sys
from asgiref.sync import sync_to_async
from game.MatchMaker import LobbyGame
from users.models import User
from tournament.models import Tournament
# from game.apps import GameConfig as app



def eprint(*args):
    print(*args, file=sys.stderr)


class LiveTournamentException(Exception):
    pass

class LiveTournament:
    __id_counter = 0
    gameConnectorFactory: callable = None
    gameManager: callable = None

    @classmethod
    def set_gameconnector_initializer(cls, gameConnectorClass):
        if not cls.gameConnectorFactory:
            cls.gameConnectorFactory = gameConnectorClass
    @classmethod
    def set_gamemanager_initializer(cls, gameManagerRef):
        if not cls.gameManager:
            cls.gameManager = gameManagerRef
    @classmethod
    def get_id(cls):
        cls.__id_counter += 1
        return cls.__id_counter

    def __init__(self, tconn, initLobbyGame: LobbyGame, match_maker):
        eprint('LiveTournament :: initializing tournament.')
        self.__match_maker = match_maker
        self.__id = self.get_id()
        self.__tconn = tconn

        # Pseudo lobby only used as tournamanent initializer
        self.__init_lobby = initLobbyGame

        self._groupA: LobbyGame = None
        self._groupB: LobbyGame = None
        self._groupC: LobbyGame = None

        self._groupAWinner = None
        self._groupBWinner = None
        self._groupCWinner = None

        self._is_closing = False

        self.__brackets = self.__get_bracket_template()


    def __contains__(self, user: User):
        return user in self.__init_lobby

    @property
    def init_lobby(self):
        return self.__init_lobby

    @property
    def first_stage_started(self):
        return self._groupA is not None and self._groupB is not None
    @property
    def is_first_stage(self):
        return self.first_stage_started is not None and self._groupC is None
    @property
    def is_second_stage(self):
        return self._groupC is not None
    @property
    def tournament(self):
        return self.__tconn.tournament
    @property
    def is_empty(self):
        return self.__init_lobby.is_empty

    @property
    def connector(self):
        return self.__tconn

    @property
    def is_setup(self):
        return self.__init_lobby and self._groupA and self._groupB
    property
    def is_finished(self):
        return self._groupC\
            and self._groupC.game_connector\
            and self._groupC.game_connector.game\
            and self._groupC.game_connector.game.winner

    # def add_member(self, user: User):
    #     self.tournament.add_member(user)

    def build_match_maker_form(self, eventID, groupID):
        return {
            'gameMode': 'Multiplayer',
            'gameType': 'Pong',
            'withAI': False,
            'eventID': str(eventID) + str(groupID),
        }

    @sync_to_async
    def setup_game_lobbies_start(self):
        if not self.__init_lobby:
            raise ValueError('LiveTournament trying to setup_game_lobbies_start() while not initLobby exist')
        formStage1A = self.build_match_maker_form(self.__init_lobby.sockID, 'A')
        formStage1B = self.build_match_maker_form(self.__init_lobby.sockID, 'B')

        plys = self.__init_lobby.players

        # if len(plys) != 2:
        if len(plys) != 4:
            raise ValueError(f'LiveTournament trying to setup_game_lobbies_start while missing players in init_lobby ({len(plys)}).')

        eprint('setup_game_lobbies_start :: players : ', plys)
        for ply in plys:
            self.tournament.add_member(ply.user)

        players = self.__init_lobby.players

        for ply in players[:2]:
            self._groupA = self.__match_maker.join_lobby(ply.user, formStage1A)
        for ply in players[2:]:
            self._groupB = self.__match_maker.join_lobby(ply.user, formStage1B)

        eprint('GroupA players: ', players[:2])
        eprint('GroupB players: ', players[2:])
        eprint('GroupA players in lobby : ', self._groupA.players)
        eprint('GroupB players in lobby : ', self._groupB.players)

        ## ... Start both tournament games
        # self.tournament.addGroupAGame(self._groupA)
        # self.tournament.addGroupBGame(self._groupB)
        # self.tournament.declare_started()

        # self.__tconn.send_connect_msg(self._groupA)
        # self.__tconn.send_connect_msg(self._groupB)

        ### send_connect_msg() called just after return from this function on for both games.
        return (self._groupA, self._groupB)

    def get_player_game(self, user: User):
        lgame = self.__init_lobby

        if self._groupC and user in self._groupC:
            lgame = self._groupC
        elif self._groupA and user in self._groupA:
            lgame = self._groupA
        elif self._groupB and user in self._groupB:
            lgame = self._groupB
        # else:
        #     raise LiveTournamentException("Trying to connect_player to LiveTournament, but either the tournament hasn't been setup properly or The player isn't a member of any toiurnament game.")
        return lgame

    def won_first_game(self, user: User) -> bool:
        eprint('LiveTournament :: check if won_first_game ')
        eprint(f'LiveTournament :: {user.login} is in groupA ', user in self._groupA)
        eprint(f'LiveTournament :: {user.login} is in groupB ', user in self._groupB)
        eprint(f'LiveTournament :: groupA : ', self._groupA)
        eprint(f'LiveTournament :: groupB : ', self._groupB)

        if user in self._groupA:
            lgame = self._groupA
        elif user in self._groupB:
            lgame = self._groupB
        else:
            return None


        if lgame and lgame.game_connector and lgame.game_connector.game and (lgame.game_connector.game.winner == user.id):
            return lgame
        return None

    def won_tournament(self, user: User) -> bool:
        if not (user in self.__init_lobby):
            return False
        lgame = self._groupC
        if lgame and lgame.game_connector and lgame.game_connector.game:
            return (lgame.game_connector.game.winner == user.id)
        return False

    async def join_final_game(self, user: User):
        eprint(f'LiveTournament :: join_final_game :: USER {user.login} TRYING TO JOIN FINAL GAME !!')
        if user in self._groupA:
            won_game = self._groupA
            self._groupAWinner = user.id
        elif user in self._groupB:
            won_game = self._groupB
            self._groupBWinner = user.id

        # if not won_game:
        #     raise LiveTournamentException(f"LiveTournament :: User {user.login} trying to join final game, but didn't win its first game.")

        eprint(f'LiveTournament :: join_final_game :: USER {user.login} won first game : won_game : ', won_game)

        formStage1C = self.build_match_maker_form(self.__init_lobby.sockID, 'C')
        if not self._groupC:
            eprint(f'LiveTournament :: join_final_game :: Creating groupC game.')
            # won_game.remove_user(user)
            # self.__match_maker.remove_player(user)
            self._groupC = self.__match_maker.join_lobby(user, formStage1C)
        else:
            self.__match_maker.join_lobby(user, formStage1C)

        await self.connector.send_stage_initializer_to_finale_user(self._groupC, user)



    def connect_player(self, user: User):
        eprint('LiveTournament :: trying to connect_player to tournament.')
        lgame = self.get_player_game(user)
        if not lgame:
            raise LiveTournamentException('LiveTournament :: Trying to connect player to tournament game, but player not in tournament.')
        lgame.set_player_connected(user)
        eprint('LiveTournament :: connect_player :: lgame : ', lgame)

        # lply = lgame.get_player(user)
        # lply.is_connected = True
        return lgame


    async def _forced_disconnect_all(self, quitter=None):#, lgame: LobbyGame):
        ### Called when a player leaves mid game.
        eprint('LiveTournament :: trying to _forced_disconnect_all() players from tournament.')
        self._is_closing = True # important

        if self.__init_lobby and self.__init_lobby.game_connector:
            eprint('LiveTournament :: trying to disconnect_all_players() players from __init_lobby.')
            await self.__init_lobby.game_connector.disconnect_all_players(quitter=quitter)
        if self._groupA and self._groupA.game_connector:
            eprint('LiveTournament :: trying to disconnect_all_players() players from groupA.')
            await self._groupA.game_connector.disconnect_all_players(quitter=quitter)
        if self._groupB and self._groupB.game_connector:
            eprint('LiveTournament :: trying to disconnect_all_players() players from groupB.')
            await self._groupB.game_connector.disconnect_all_players(quitter=quitter)
        if self._groupC and self._groupC.game_connector:
            eprint('LiveTournament :: trying to disconnect_all_players() players from groupC.')
            await self._groupC.game_connector.disconnect_all_players(quitter=quitter)

        # if lgame.game_connector:
        #     for ply in lgame.players:
        #         lgame.game_connector.disconnect_player(ply.user)


    def _soft_disconnect(self, lgame: LobbyGame, user: User):
        ### Called when player leaves either after losing first game or after tournament conclusion.
        pass


    # def __disconnect_was_early(self, user: User):
    #     pass

    def __player_is_looser_of_first_game(self, user: User):
        if not self._groupA or self._groupB:
            return False
        lgame = self.__init_lobby
        if user in self._groupA and lgame.sockID == self._groupA.sockID:
            lgame = self._groupA
        elif user in self._groupB and lgame.sockID == self._groupB.sockID:
            lgame = self._groupB
        return lgame != self.__init_lobby and not self._groupC or not (user in self._groupC) and lgame.is_over and user.id != lgame.winner

    def __player_reached_end_game(self, user):
        if not (self._groupC and user in self._groupC):
            return False
        gconn = self._groupC.game_connector
        game = gconn.game
        if not game:
            return False
        return game.is_over

    def __player_is_winner_of_first_game(self, user):
        return user.id == self._groupAWinner or user.id == self._groupBWinner
    def __player_is_winner_of_tournament(self, user):
        return user.id == self._groupCWinner


    async def disconnect_player(self, user: User):
        ''' Returns True or False to signal if the tournament should be shutdown or not. '''

        ## TODO: LOTS OF WORK TO DO ::: build switch with all disconnect scenarios.
        eprint('LiveTournament :: disconnect_player :: Trying to disconnect ', user.login)
        eprint('LiveTournament :: disconnect_player :: user in self.__init_lobby : ', user in self.__init_lobby)
        eprint('LiveTournament :: disconnect_player :: first_stage_started : ', self.first_stage_started)
        if user in self.__init_lobby and not self.first_stage_started:
            ''' Player disconnecting from tournament lobby. '''
            eprint('LiveTournament :: user in self.__init_lobby and not self.first_stage_started : TRUE')
            self.__match_maker.remove_player(user)
            await self.__init_lobby.game_connector.disconnect_player(user)
            return False
            # self.__init_lobby.remove_user(user)

        lgame = self.get_player_game(user)
        if not lgame.game_connector:
            eprint('LiveTournament :: lgame has no game connector')
            return False

        gconn = lgame.game_connector

        if gconn.game and gconn.game.is_running:
            ''' If game is running, force disconnect all players from tournament.'''
            # eprint('LiveTournament :: force_disconnect_all_player :: init_lobby : ', self.__init_lobby)
            # await self._forced_disconnect_all(user.id)
            if user in lgame:
                eprint('LiveTournament :: Sending quitter signal through tournament Websocket.')
                await self.__tconn.disconnect_player(user)
                await self.__tconn.send_quitter_signal(user)

                await self.__tconn.tournament.force_shutdown()
                await gconn.disconnect_player(user)

                # await gconn.disconnect_player(user, user.id)
                eprint('LiveTournament :: force_disconnect_all_player :: flushing user from match_maker.')
                self.__match_maker.remove_player_from(user, lgame)
                self.__match_maker.remove_player_from(user, self.__init_lobby)
            # lgame.game_connector.disconnect_player(user)
            return self.is_empty



        ### Manage regular routes first : looser diconnect from first game.
        if self.__player_is_looser_of_first_game(user):
            eprint('LiveTournament :: __player_is_looser_of_first_game and disconnecting')
            eprint('LiveTournament :: lgame is init lobby : ', lgame == self.__init_lobby)
            eprint('LiveTournament :: lgame.is_over : ', lgame.is_over)
            await gconn.disconnect_player(user)
            await self.__tconn.disconnect_player(user)
            if user in lgame:
                self.__match_maker.remove_player_from(user, lgame)
                self.__match_maker.remove_player_from(user, self.__init_lobby)
            return False
        ### Manage regular routes first : winner/looser diconnect from final game.
        elif self.__player_reached_end_game(user):
            eprint('LiveTournament :: __player_reached_end_game and disconnecting')
            self._is_closing = True
            gconn = lgame.game_connector
            await gconn.disconnect_player(user)
            await self.__tconn.disconnect_player(user)
            if user in lgame:
                self.__match_maker.remove_player_from(user, lgame)
                self.__match_maker.remove_player_from(user, self.__init_lobby)
            return self.is_empty

        elif self.__player_is_winner_of_first_game(user):
            eprint('LiveTournament :: __player_is_winner_of_first_game and disconnecting')
            if user in self._groupA:
                gconn = self._groupA.game_connector
                if gconn:
                    self._update_brackets_info('groupA', self._groupA)
                    await gconn.disconnect_player(user)
                    self.__match_maker.remove_player_from(user, self._groupA)
            elif user in self._groupB:
                gconn = self._groupB.game_connector
                if gconn:
                    self._update_brackets_info('groupB', self._groupB)
                    await gconn.disconnect_player(user)
                    self.__match_maker.remove_player_from(user, self._groupA)
            return False

        # elif self.__player_is_winner_of_tournament(user):
        #     if user in self._groupC:
        #         gconn = self._groupC.game_connector
        #         if gconn:
        #             self._update_brackets_info('groupC', self._groupC)
        #             await gconn.disconnect_player(user)
        #         await self.__tconn.disconnect_player(user)
        #     # return self.

        else:
            eprint('LiveTournament :: player disconnecting from tournament in an unforeseen manner.')

        return False
        # if lgame:
        #     if lgame.is_running:
        #         return self._forced_disconnect_all(lgame)
        #     elif lgame.winner == user.id:
        #         return self._forced_disconnect_all(lgame)
        #     else:
        #         return self._soft_disconnect(lgame, user)



        #     lgame.remove_user(user)
        #     if lgame.game_connector and lgame.game_connector.game.is_running:
        #         lgame.game_connector.disconnect_player(user)

        #     ### Return True if live tournament should be SHUTDOWN.
        #     if lgame.is_empty:
        #         ## shutdown tournament
        #         return True
        #     else:
        #         return False
        # else:
        #     return True


    # async def connect_player(self, user: User, consumer):

    #     if self._groupA and user in self._groupA:
    #         lgame = self._groupA
    #     elif self._groupB and user in self._groupB:
    #         lgame = self._groupB
    #     elif self._groupC and user in self._groupC:
    #         lgame = self._groupC
    #     else:
    #         raise LiveTournamentException("Trying to connect_player to LiveTournament, but either the tournament hasn't been setup properly or The player isn't a member of any toiurnament game.")

    #     # if not lgame.game_connector:
        #     gconn = self.gameConnectorFactory(lgame.sockID)
        #     lgame.set_game_connector(gconn)
        #     gconn.set_lobby_game(lgame)
        # else:
        #     gconn = lgame.game_connector


        # await gconn.connect_player(consumer.user, consumer, is_tournament_stage=True)
        # await gconn.send_init_state(self.gameManager.getInitInfo(lgame.gameType))

        # await self.__tconn.send_brackets(self.get_brackets_info())


    def __get_bracket_template(self):
        return {
            'groupA': {
                'p1': {
                    'login': None,
                    'score': '-',
                    'won': False
                },
                'p2': {
                    'login': None,
                    'score': '-',
                    'won': False
                },
            },
            'groupB': {
                'p3': {
                    'login': None,
                    'score': '-',
                    'won': False
                },
                'p4': {
                    'login': None,
                    'score': '-',
                    'won': False
                },
            },
            'groupC': {
                'winner1': {
                    'login': None,
                    'score': '-',
                    'won': False
                },
                'winner2': {
                    'login': None,
                    'score': '-',
                    'won': False
                },
            }
        }

    def update_brackets_info(self, group, lgame):
        players = lgame.players
        if group == 'groupA':
            self.__brackets['p1']['login'] = players[0].user.login
            self.__brackets['p2']['login'] = players[1].user.login
            self.__brackets['p1']['won'] = (players[0].user.id == self._groupAWinner)
            self.__brackets['p2']['won'] = (players[1].user.id == self._groupAWinner)
        elif group == 'groupB':
            self.__brackets['p3']['login'] = players[0].user.login
            self.__brackets['p4']['login'] = players[1].user.login
            self.__brackets['p3']['won'] = (players[0].user.id == self._groupBWinner)
            self.__brackets['p4']['won'] = (players[1].user.id == self._groupBWinner)
            pass
        elif group == 'groupC':
            self.__brackets['p1']['login'] = players[0].user.login
            self.__brackets['p2']['login'] = players[1].user.login
            self.__brackets['p1']['won'] = (players[0].user.id == self._groupAWinner)
            self.__brackets['p2']['won'] = (players[1].user.id == self._groupAWinner)

        # self.__tconn.send_brackets(self.__brackets)


    def get_brackets_info(self):
        return self.__brackets
        # brackets = self.__get_bracket_template()
        # plys_list = self.__init_lobby.players

        # if not self._groupA or self._groupB or not self._groupA.game_connector or not self._groupB.game_connector:
        #     return None

        # if self._groupA:
        #     gconnA = self._groupA.game_connector
        #     gameA = gconnA.game
        #     if gameA.winner == plys_list[0].id:
        #         winnerA = plys_list[0]
        #         brackets['groupA']['p1']['won'] = True
        #     elif gameA.winner == plys_list[1].id:
        #         winnerA = plys_list[1]
        #         brackets['groupA']['p2']['won'] = True

        # if self._groupB:
        #     gconnB = self._groupB.game_connector
        #     gameB = gconnB.game
        #     if gameB.winner == plys_list[2].id:
        #         winnerB = plys_list[2]
        #         brackets['groupB']['p3']['won'] = True
        #     elif gameB.winner == plys_list[3].id:
        #         winnerB = plys_list[3]
        #         brackets['groupB']['p4']['won'] = True

        # if self._groupC:
        #     gconnC = self._groupC.game_connector
        #     gameC = gconnC.game
        #     if gameC.winner == winnerA.id:
        #         winnerC = winnerA
        #         brackets['groupC']['winner1']['won'] = True
        #     elif gameC.winner == winnerB.id:
        #         winnerC = winnerB
        #         brackets['groupC']['winner2']['won'] = True

        # if len(plys_list) > 0:
        #     brackets['groupA']['p1']['login'] = plys_list[0].user.login
        # elif len(plys_list) > 1:
        #     brackets['groupA']['p2']['login'] = plys_list[1].user.login
        # elif len(plys_list) > 2:
        #     brackets['groupB']['p3']['login'] = plys_list[2].user.login
        # elif len(plys_list) > 3:
        #     brackets['groupB']['p4']['login'] = plys_list[3].user.login

        # return brackets



    # def __contains__(self, game: LobbyGame):
    #     return next((True for g in self if g == game), False)

    # def __iter__(self):
    #     if self._groupA:
    #         yield self._groupA
    #     if self._groupB:
    #         yield self._groupB
    #     if self._groupC:
    #         yield self._groupC

    # def __repr__(self):
    #     return f"Tournament {self.__id}, {self.__tconn}"

    # @property
    # def id(self):
    #     return self.__id

    # @property
    # def tconn(self):
    #     return self.__tconn

    # @tconn.setter
    # def tconn(self, value):
    #     self.__tconn = value

    # @property
    # def groupA(self):
    #     return self._groupA

    # @groupA.setter
    # def groupA(self, value):
    #     self._groupA = value

    # @property
    # def groupB(self):
    #     return self._groupB

    # @groupB.setter
    # def groupB(self, value):
    #     self._groupB = value

    # @property
    # def groupC(self):
    #     return self._groupC

    # @groupC.setter
    # def groupC(self, value):
    #     self._groupC = value

    # @property
    # def is_full_R1(self):
    #     return self._groupA and self._groupB

    # @property
    # def is_full_R2(self):
    #     return self._groupC

#    @property
#    def is_readyR1(self):
#        return not self._groupA.is_ready and self._groupB.is_ready

#     @property
#     def is_readyR2(self):
#         return not self._groupC.is_ready




    #  SETTER  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    #  EVENTS  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

