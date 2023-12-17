
from game.MatchMaker import LobbyGame

class LiveTournament:
    __id_counter = 0

    def __init__(self, tconn, initLobbyGame: LobbyGame):

        self.__id = self.get_id()
        self.__tconn = tconn

        # Pseudo lobby only used as tournamanent initializer
        self.__init_lobby = initLobbyGame
        
        self._groupA: LobbyGame = None
        self._groupB: LobbyGame = None
        self._groupC: LobbyGame = None

    @classmethod
    def get_id(cls):
        cls.__id_counter += 1
        return cls.__id_counter
    
    @property
    def init_lobby(self):
        return self.__init_lobby
    
    @property
    def is_first_stage(self):
        return self._groupC is None
    @property
    def is_second_stage(self):
        return self._groupC is not None

    @property
    def connector(self):
        return self.__tconn

    # def build_brackets_info(self):
    #     pass # return the define bracket in def
        
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
    
    