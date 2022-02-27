"""Contains an object for iterating rounds of a game of Prisoner's Dilemma"""

from typing import List, Tuple
from Dna import Dna
from Player import Player, initialize_players

class PDGame:
    """Stores information about a game of Prisoner's Dilemma.
    Stores two players and the current round out of a given integer.
    There are also class variables for the scoring system."""
    TEMPTATION :int = 5
    REWARD :int = 3
    PENALTY :int = 1
    SUCKER :int = 0

    __slots__ = ['p1', 'p2', 'rounds', 'curRound']
    def __init__(self, p1:Player, p2:Player, rounds:int=64):
        """Creates a game of Prisoner's Dilemma with the given players
        for the given number of rounds."""
        self.p1 :Player = p1
        self.p2 :Player = p2
        initialize_players(p1, p2)
        self.rounds :int = rounds
        self.curRound :int = 1

    def __iter__(self): return self

    def __str__(self) -> str:
        return "<PDGame "+str(self.p1)+" vs "+str(self.p2)+">"

    def play(self)->str:
        """Plays a single round of Prisoner's Dilemma and returns the moves of p1 and p2 as a string"""
        if self.curRound > self.rounds: raise StopIteration
        res :str = self.p1.getMove() + self.p2.getMove()
        if   res == "CC":
            self.p1.score += PDGame.REWARD
            self.p2.score += PDGame.REWARD
            self.p1.updateHistory("R")
            self.p2.updateHistory("R")
        elif res == "CD":
            self.p1.score += PDGame.SUCKER
            self.p2.score += PDGame.TEMPTATION
            self.p1.updateHistory("S")
            self.p2.updateHistory("T")
        elif res == "DC":
            self.p1.score += PDGame.TEMPTATION
            self.p2.score += PDGame.SUCKER
            self.p1.updateHistory("T")
            self.p2.updateHistory("S")
        elif res == "DD":
            self.p1.score += PDGame.PENALTY
            self.p2.score += PDGame.PENALTY
            self.p1.updateHistory("P")
            self.p2.updateHistory("P")
        else: raise Exception("How tf did you manage this?")
        self.curRound += 1
        return res
    __next__ = play

    def playAll(self)->Tuple[int,int]:
        """Plays all the remaining rounds left to play and returns the final score for both players"""
        all(self)
        return self.p1.score, self.p2.score
    __call__ = playAll

    @classmethod
    def highestPossibleScore (cls, rounds:int)->int:
        """Returns the highest possible score a player can achieve given the number of `rounds`"""
        return max(cls.TEMPTATION, cls.SUCKER, cls.REWARD, cls.PENALTY) * rounds

    @classmethod
    def lowestPossibleScore (cls, rounds:int)->int:
        """Returns the lowest possible score a player can achieve given the number of `rounds`"""
        return min(cls.TEMPTATION, cls.SUCKER, cls.REWARD, cls.PENALTY) * rounds

def oneVersusMany (p1:Player, l2 :List[Dna], *args, **kwargs)->int:
    """Makes the given player `p1` play against a list of DNAs `l2`.
    Returns the total score `p1` achieved from every opponent.
    Will use the given number of rounds if given or use the default."""
    return sum((PDGame(p1, Player.from_dna(d2), *args, **kwargs)()[0] for d2 in l2))

def manyVersusMany (l1:List[Dna], l2:List[Dna], *args, **kwargs)->List[int]:
    """Makes the given list of DNAs `l1` play against the other given list `l2`.
    Returns a list of the total scores each player in `l1` scored from every opponent in `l2`.
    Will use the given number of rounds if given or use the default."""
    return [oneVersusMany(Player.from_dna(d1), l2, *args, **kwargs) for d1 in l1]

def manyVersusOne (l1:List[Dna], p2:Player, *args, **kwargs)->List[int]:
    """Makes the given list of DNAs `l1` play against the a given player `p2`.
    Returns a list of the scores each player in `l1` scored against `p2`.
    Will use the given number rounds if given or use the default."""
    return [PDGame(Player.from_dna(d1), p2, *args, **kwargs)()[0] for d1 in l1]

