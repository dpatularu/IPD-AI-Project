
from mimetypes import init
import random
from typing import Callable, Union
from Generators import CD_Generator



class Player:
    outcomes :dict = { v:k for k,v in enumerate("RTSP") } # factors as dictionary
    nodeSize :int = len(outcomes)

    def __init__ (self, memDepth :int,
    strat :Union[str,Callable[[int],str]] = CD_Generator.random,
    initMoves :Union[str,Callable[[int],str]] = CD_Generator.random):
        """Creates a new player with the given memory depth, strategy,
        and initial moves.

        Remember to initialize the player before playing the game.
        Use the initializePlayers function in this module.
        
        Parameters
        ----------
        `memDepth` : int
            The memory depth of this player, or, the number of rounds they will remember
        `strat` : str  |  (int) -> str
            The strategy of this player, can be a str of length `memDepth` or a function
        that takes an int and returns a string.
        `initMoves` : str | (int) -> str
            The initial moves this player will use to prepopulate the history.
        Can be a string or a function that takes an int and returns a string.
        """
        self.memDepth = memDepth
        self.stratSize = self.nodeSize ** self.memDepth
        # Initialize initial moves
        if isinstance(initMoves, str):
            self.initMoves :str = initMoves
        else:
            self.initMoves :str = initMoves(self.memDepth)
        assert len(self.initMoves) == self.memDepth, "Length of initial moves must equal memory depth"
        self.curState :str = "." * self.memDepth # Starts empty, needs initializing
        # Initialize strategy
        if isinstance(strat, str):
            self.strategy :str = strat
        else:
            self.strategy :str = strat(self.stratSize)
        # Can also check if strategy is valid (consists only of letters from `factors`)
        assert self.stratSize == len(self.strategy), "Length of strategy string must equal nodeSize^memDepth"
        self.score :int = 0 # Player wants to maximize this

    def encodeHistory (self)->int:
        """Encodes the current state into an int from [0,`stratSize`)"""
        result :int = 0
        step : int = self.stratSize / self.nodeSize # Value of last 'bit'
        for i in range(self.memDepth):
            result += step * self.outcomes[self.curState[i]]
            step /= self.nodeSize
        return int(result)

    def getMove (self)->str:
        """Returns whether this player would C or D for the current history and strategy"""
        if self.curState[0]=='.':
            print("Error, player was not itialized yet!")
            exit(-1)
        return self.strategy[self.encodeHistory()]
    
    def updateHistory (self, outcome:str):
        """Updates the history with the oponents `newState`"""
        self.curState = self.curState[1:] + outcome



def initializePlayers (p1:Player, p2:Player):
    """Prepopulate the history of both given players using their initial moves"""
    p1M = len(p1.initMoves)
    p2M = len(p2.initMoves)
    M = max(p1M, p2M)
    for m in range(M):
        p1m = p1.initMoves[m] if m < p1M else p1.getMove()
        p2m = p2.initMoves[m] if m < p2M else p2.getMove()
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
