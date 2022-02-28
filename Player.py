"""Contains the Player class and also related functions

Dna of a Player is strategy CONCAT initMoves
- So 'CCDCD' would initially defect and always cooperate unless they were a sucker last round
- So 'CCDCD' would be a strategy ID of 4 and an initMoves ID of 1 with an overall ID of 9
"""

from typing import Tuple
from Dna import Dna


class Player:
    OUTCOMESA :list = ["R", "T", "S", "P"]
    OUTCOMESD :dict = { v:k for k,v in enumerate(OUTCOMESA) } # factors as dictionary
    NODESIZE :int = len(OUTCOMESA)
    NODEDEPTH :int = NODESIZE.bit_length()-1 # log_2 (NODESIZE)

    __slots__ = ['initMoves', 'strategy', 'curState', 'initialized', 'score']
    def __init__ (self, strategy:Dna, initialMoves:Dna):
        """Creates a player using the given strategy and initial moves"""
        self.initMoves :Dna = initialMoves
        self.strategy  :Dna = strategy
        if Player.NODESIZE**self.memDepth != self.stratSize: raise ValueError
        self.curState :int = 0 # Starts empty, needs initializing
        self.initialized :bool = False
        self.score :int = 0 # Player wants to maximize this
    
    @property
    def memDepth (self)->int:
        """Returns the memory depth of this player"""
        return self.initMoves.size
    
    @memDepth.setter
    def memDepth (self, m:int):
        """Sets the memory depth of this Player, fills """
        if m <= 0 or m > 12: raise ValueError
        self.initMoves.size = m
        self.strategy.size = Player.NODESIZE ** m
    
    @property
    def stratSize (self)->int:
        """Returns the number of bits needed to store this Player's strategy"""
        return self.strategy.size
    
    @stratSize.setter
    def stratSize (self, s:int):
        if s < Player.NODESIZE or s%4!=0 or s.bit_length()%2!=1: raise ValueError
        self.strategy.size = s
        self.initMoves.size = s.bit_length().bit_length()-1 # math.log can eat my ass

    @classmethod
    def calcStratSize (cls, memDepth:int)->int:
        """Returns the number of bits needed to store a strategy with memory depth `memDepth`"""
        return cls.NODESIZE**memDepth

    @staticmethod
    def __split__(d:Dna)->Tuple[Dna,Dna]:
        s :int = 1<<(d.size.bit_length()-1)
        S :str = str(d)
        return (Dna(S[:s]), Dna(S[s:]))

    @staticmethod
    def __combine__(d1:Dna, d2:Dna)->Dna:
        return Dna(str(d1)+str(d2))

    @classmethod
    def from_str (cls, strategy:str, initialMoves:str):
        """Constructs a player using the two strings `strategy` and `initialMoves`.

        For example, ("DDDD", "C"), would construct a player who initially cooperates but always defects.
        """
        return cls(Dna(strategy), Dna(initialMoves))

    @classmethod
    def from_dna (cls, d:Dna):
        """Constructs a player using the given Dna `d`.
        The Dna object is appropriately split into a strategy and initial move(s). Check Dna for more info.
        """
        (d1, d2) = Player.__split__(d)
        return cls(d1, d2)

    @classmethod
    def from_id (cls, memoryDepth:int, id:int):
        """Creates a Player using the given `memoryDepth` and `id`.
        
        `id` is an integer where each bit represents a C or D.
        
        For example, with a memDepth of 1, an id of 3 would be a
        strategy of 'DCCC' and initMove of 'D'."""
        (d1, d2) = Player.__split__(Dna(id, cls.calcStratSize(memoryDepth)+memoryDepth))
        return cls(d1, d2)

    def getMove (self)->str:
        """Returns whether this player would C or D for the current history and strategy"""
        if not self.initialized:
            raise Exception("Player not initialized yet")
        return "D" if self.strategy[self.curState] else "C"
        
    def updateHistory (self, outcome:str):
        """Updates the history with the result of last round"""
        self.curState = (self.curState << Player.NODEDEPTH | Player.OUTCOMESD[outcome]) % len(self.strategy)

    def __str__ (self):
        return str(self.strategy) + str(self.initMoves)

    def __eq__(self, o) -> bool:
        if isinstance(o, Player):
            return self.strategy==o.strategy and self.initMoves==o.initMoves and self.curState==o.curState
        elif isinstance(o, Dna):
            return o == str(self)
        elif isinstance(o, str):
            return str(self) == o
        elif isinstance(o, int):
            return o == (self.strategy.val << self.initMoves.size) | self.initMoves.val
        else: raise ValueError        

    def curState_str (self)->str:
        """String representation of this player's current state, or memory"""
        s :int = self.curState
        result :str = ""
        for i in range(self.memDepth):
            result += Player.OUTCOMESA[s&3]
            s >>= 2
        return result

def initialize_players (p1:Player, p2:Player):
    """Prepopulate the history of both given players using their initial moves"""
    p1.score = 0
    p2.score = 0
    M = max(p1.memDepth, p2.memDepth)
    p1.initialized = True
    p2.initialized = True
    for m in range(M):
        p1m = ("D" if p1.initMoves[m] else "C") if m < p1.memDepth else p1.getMove()
        p2m = ("D" if p2.initMoves[m] else "C") if m < p2.memDepth else p2.getMove()        
        result = p1m + p2m
        if result == "CC":
            p1.updateHistory("R")
            p2.updateHistory("R")
        elif result == "DC":
            p1.updateHistory("T")
            p2.updateHistory("S")
        elif result == "CD":
            p1.updateHistory("S")
            p2.updateHistory("T")
        elif result == "DD":
            p1.updateHistory("P")
            p2.updateHistory("P")
        else: raise ValueError
