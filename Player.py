"""Contains the Player class and also related functions

Dna of a Player is strategy CONCAT initMoves
- So 'CCDCD' would initially defect and always cooperate unless they were a sucker last round
- So 'CCDCD' would be a strategy ID of 4 and an initMoves ID of 1 with an overall ID of 9
"""

from typing import Tuple
from Dna import Dna, Dna4
from Node import CD, RSTP


class Player:

    __slots__ = ['initMoves', 'strategy', 'curState', 'initialized', 'score']
    def __init__(self, strategy: Dna, initialMoves: Dna):
        """Creates a player using the given strategy and initial moves"""
        self.initMoves: Dna = initialMoves
        self.strategy: Dna = strategy
        if self.calcStratSize(self.memDepth) != self.stratSize:
            raise ValueError("Strat size and memory depth don't work together")
        self.curState: Dna4 = Dna4(0, len(initialMoves))  # Starts empty, needs initializing
        self.initialized: bool = False
        self.score: int = 0  # Player wants to maximize this

    @property
    def memDepth(self) -> int:
        """Returns the memory depth of this player"""
        return self.initMoves.size

    @memDepth.setter
    def memDepth(self, m: int):
        """Sets the memory depth of this Player, fills """
        if m <= 0 or m > 12: raise ValueError("Bad memory depth, must be a small whole number")
        self.initMoves.size = m
        self.strategy.size = self.calcStratSize(m)

    @property
    def stratSize(self) -> int:
        """Returns the number of bits needed to store this Player's strategy"""
        return self.strategy.size

    @stratSize.setter
    def stratSize(self, s: int):
        if s < Dna4.NODESIZE or s % Dna4.NODESIZE != 0:
            raise ValueError("Bad strat size, must be a power of", Dna4.NODESIZE)
        self.strategy.size = s
        self.initMoves.size = s.bit_length().bit_length() - 1  # math.log can eat my ass

    @staticmethod
    def calcStratSize(memDepth: int) -> int:
        """Returns the number of bits needed to store a strategy with memory depth `memDepth`"""
        return 2 ** (RSTP.size()*memDepth)

    @staticmethod
    def calcDnaSize(memDepth: int) -> int:
        """Returns the number of bits needed to store the DNA of a player with memory depth `memDepth`"""
        return Player.calcStratSize(memDepth) + memDepth

    @staticmethod
    def __split__(d: Dna) -> Tuple[Dna, Dna]:
        memDepth: int = (d.size.bit_length() - 1)//2  # Log4 of size
        stratSize :int = Player.calcStratSize(memDepth)
        assert len(d) - stratSize - memDepth == 0, "Given DNA wouldn't split up nicely becuase of its size"
        return Dna(d.val>>memDepth, stratSize), Dna(d.val & (2**memDepth-1), memDepth)

    @staticmethod
    def __combine__(d1: Dna, d2: Dna) -> Dna:
        return Dna(str(d1) + str(d2))

    @classmethod
    def from_str(cls, strategy: str, initialMoves: str):
        """Constructs a player using the two strings `strategy` and `initialMoves`.

        For example, ("DDDD", "C"), would construct a player who initially cooperates but always defects.
        """
        return cls(Dna(strategy), Dna(initialMoves))

    @classmethod
    def from_dna(cls, d: Dna):
        """Constructs a player using the given Dna `d`.
        The Dna object is appropriately split into a strategy and initial move(s). Check Dna for more info.
        """
        return cls(*Player.__split__(d))

    @classmethod
    def from_id(cls, memoryDepth: int, id: int):
        """Creates a Player using the given `memoryDepth` and `id`.
        
        `id` is an integer where each bit represents a C or D.
        
        For example, with a memDepth of 1, an id of 3 would be a
        strategy of 'DCCC' and initMove of 'D'."""
        return cls(
            Dna(id>>memoryDepth, cls.calcStratSize(memoryDepth)),
            Dna(id & (2**memoryDepth-1), memoryDepth)
        )

    def getMove(self) -> CD:
        """Returns whether this player would defect or coopperate for the current history and strategy"""
        if not self.initialized: raise Exception("Player not initialized yet")
        return self.strategy.getCD(int(self.curState))

    # TODO: Cache results of arguments (strat,curState)? But if a cache hit occurs, that's a loop, algo to recognize and optimize?
    def updateHistory(self, outcome: RSTP):
        """Updates the history with the result of last round"""
        self.curState >>= outcome

    def __str__(self): return str(self.strategy) + str(self.initMoves)

    def __int__(self): return (int(self.strategy) << self.initMoves.size) | int(self.initMoves)

    def __eq__(self, o) -> bool:
        if isinstance(o, Player):
            return self.strategy == o.strategy and self.initMoves == o.initMoves
        elif isinstance(o, Dna):
            return int(self) == int(o)
        elif isinstance(o, str):
            return str(self) == o
        elif isinstance(o, int):
            return int(self) == o
        else: raise TypeError("Cannot compare(==) against",type(o))

#================================================================================================================================

def initialize_players(p1: Player, p2: Player):
    """Prepopulate the history of both given players using their initial moves"""
    p1.score = 0
    p2.score = 0
    M = max(p1.memDepth, p2.memDepth)
    p1.initialized = True
    p2.initialized = True
    for m in range(M):
        p1m = str(p1.initMoves[m] if m < p1.memDepth else p1.getMove())
        p2m = str(p2.initMoves[m] if m < p2.memDepth else p2.getMove())
        result = p1m + p2m
        if result == "CC":
            p1.updateHistory(RSTP.R)
            p2.updateHistory(RSTP.R)
        elif result == "DC":
            p1.updateHistory(RSTP.T)
            p2.updateHistory(RSTP.S)
        elif result == "CD":
            p1.updateHistory(RSTP.S)
            p2.updateHistory(RSTP.T)
        elif result == "DD":
            p1.updateHistory(RSTP.P)
            p2.updateHistory(RSTP.P)
        else:
            raise ValueError("Invalid outcome:",result)
