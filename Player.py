"""Contains the Player class and also related functions

CD Strings should follow the `encode_CD` and `decode_CD` functions.
Take for example 'CDCC', this would encode to 2, (or 0010 in binary).
So reverse the string, and convert C->0 and D->1, and that's your number in binary.
"""

class Player:
    OUTCOMESA :list = ["R", "T", "S", "P"]
    OUTCOMESD :dict = { v:k for k,v in enumerate(OUTCOMESA) } # factors as dictionary
    NODESIZE :int = len(OUTCOMESA)
    NODEDEPTH :int = 2 # log_2 (NODESIZE) -> int

    def __init__ (self, memoryDepth:int, strategy:int, initialMoves:int):
        """Creates a new player with the given memory depth, strategy, and initial moves.

        You can use any of the `from_<blank>` class methods to construct a Player.

        Remember to initialize the player before playing the game.
        Use the initializePlayers function that's in this file.
        """
        self.memDepth  :int = memoryDepth # In bits
        self.initMoves :int = initialMoves
        assert self.initMoves < 2**self.memDepth, "InitialMoves > highest possible value with given MemoryDepth"
        self.strategy  :int = strategy
        self.stratSize :int = Player.NODESIZE ** self.memDepth
        assert self.strategy < 2**self.stratSize, "Strategy > highest possible value with the given MemoyyDepth"
        self.curState :int = 0 # Starts empty, needs initializing
        self.stateMask :int = self.stratSize - 1 # To keep the curState small
        self.initialized :bool = False
        self.score :int = 0 # Player wants to maximize this

    @classmethod
    def from_str (cls, strategy:str, initialMoves:str):
        """Creates a Player using the given strings `strategy` and `initialMoves`
        
        The memory depth is interpreted from the length of `initialMoves`.
        The length of `strategy` should be 4**memDepth.
        """
        s :int = encode_CD(strategy)
        i :int = encode_CD(initialMoves)
        return cls(len(initialMoves), s, i)

    @classmethod
    def from_dna (cls, dna:str):
        """Creates a Player using the given string `dna`.
        
        `dna` can be thought of as strategy CONCAT initMoves.
        
        For example, 'CCCCD', is an always-cooperate player who initially defects."""
        L :int = len(dna) # Length of DNA
        s :int = 4 # Splitting index between strat and init. moves
        while s<L>>1:s<<=2 # Find where s should be with respect to L
        return cls.from_str(dna[:s], dna[s:])

    @classmethod
    def from_id (cls, memoryDepth:int, id:int):
        """Creates a Player using the given `memoryDepth` and `id`.
        
        `id` is number where each bit represents a C or D.
        
        For example, with a memDepth of 1, an id of 3 would be a
        strategy of 'DCCC' and initMove of 'D'."""
        strat :int = id >> memoryDepth
        init  :int= id & ((1 << memoryDepth) - 1)
        return cls(memoryDepth, strat, init)

    def getMove (self)->str:
        """Returns whether this player would C or D for the current history and strategy"""
        if not self.initialized:
            print("Error, player was not itialized yet!")
            exit(-1)
        return "D" if (self.strategy >> self.curState) & 1 else "C"
        
    def updateHistory (self, outcome:str):
        """Updates the history with the result of last round"""
        self.curState <<= Player.NODEDEPTH
        self.curState = self.curState & self.stateMask | Player.OUTCOMESD[outcome]
    
    def strategy_str (self)->str:
        """String representation of this player's strategy"""
        return decode_CD(self.stratSize, self.strategy)
    
    def initMoves_str (self)->str:
        """String representation of this player's initial moves"""
        return decode_CD(self.memDepth, self.initMoves)
    
    def curState_str (self)->str:
        """String representation of this player's current state, or memory"""
        s :int = self.curState
        result :str = ""
        for i in range(self.memDepth):
            result += Player.OUTCOMESA[s&3]
            s >>= 2
        return result

def decode_CD (size:int, n:int)->str:
    """Decodes the given integer `n` into a string of Cs and Ds of size `size`"""
    result :str = ""
    step :int = 1
    for m in range(size):
        result += "D" if n & step else "C"
        step <<= 1
    return result

def encode_CD (s:str)->int:
    """Encodes the CD string `s` into an integer"""
    result :int = 0
    step :int = 1
    RES :dict = {"C":False, "D":True}
    for i in range(len(s)):
        if RES[s[i]]:
            result |= step
        step <<= 1
    return result

def initialize_players (p1:Player, p2:Player):
    """Prepopulate the history of both given players using their initial moves"""
    p1.score = 0
    p2.score = 0
    p1M = p1.memDepth
    p2M = p2.memDepth
    M = max(p1M, p2M)
    for m in range(M):
        p1m = ("D" if (p1.initMoves >> m) & 1 else "C") if m < p1M else p1.getMove()
        p2m = ("D" if (p2.initMoves >> m) & 1 else "C") if m < p2M else p2.getMove()
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
        else:
            print("Error, invalid move")
            exit(-1)
    p1.initialized = True
    p2.initialized = True
