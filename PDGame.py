"""Contains an object for iterating rounds of a game of Prisoner's Dilemma"""

from typing import List, Tuple
from Dna import Dna
from Node import RSTP
from Player import Player, initialize_players
from SearchAlgorithms import coalesce


class PDGame:
    """Stores information about a game of Prisoner's Dilemma.
    Stores two players and the current round out of a given integer.
    There are also class variables for the scoring system."""
    TEMPTATION: int = 5
    REWARD: int = 3
    PENALTY: int = 1
    SUCKER: int = 0
    DEFAULT_ROUNDS: int = 64

    __slots__ = ['p1', 'p2', 'rounds', 'curRound']

    def __init__(self, p1: Player, p2: Player, rounds: int = None):
        """Creates a game of Prisoner's Dilemma with the given players
        for the given number of rounds, defaults to DEFAULT_ROUNDS."""
        self.p1: Player = p1
        self.p2: Player = p2
        initialize_players(p1, p2)
        self.rounds: int = coalesce(rounds, PDGame.DEFAULT_ROUNDS)
        self.curRound: int = 1

    def __iter__(self):
        return self

    def __str__(self) -> str:
        return "<PDGame " + str(self.p1) + " vs " + str(self.p2) + ">"

    def play(self) -> Tuple[Player, Player]:
        """Plays a single round of Prisoner's Dilemma and returns the moves of p1 and p2 as a string"""
        if self.curRound > self.rounds: raise StopIteration
        res: str = str(self.p1.getMove()) + str(self.p2.getMove())
        if res == "CC":
            self.p1.score += PDGame.REWARD
            self.p2.score += PDGame.REWARD
            self.p1.updateHistory(RSTP.Reward)
            self.p2.updateHistory(RSTP.Reward)
        elif res == "CD":
            self.p1.score += PDGame.SUCKER
            self.p2.score += PDGame.TEMPTATION
            self.p1.updateHistory(RSTP.Sucker)
            self.p2.updateHistory(RSTP.Tempted)
        elif res == "DC":
            self.p1.score += PDGame.TEMPTATION
            self.p2.score += PDGame.SUCKER
            self.p1.updateHistory(RSTP.Tempted)
            self.p2.updateHistory(RSTP.Sucker)
        elif res == "DD":
            self.p1.score += PDGame.PENALTY
            self.p2.score += PDGame.PENALTY
            self.p1.updateHistory(RSTP.Penalty)
            self.p2.updateHistory(RSTP.Penalty)
        else:
            raise Exception("How tf did you manage this?")
        self.curRound += 1
        return (self.p1, self.p2)
    __next__ = play

    def playAll(self) -> Tuple[Player, Player]:
        """Plays all the remaining rounds left to play and returns the final score for both players"""
        all(self)
        return self.p1, self.p2

    __call__ = playAll

    @classmethod
    def highestPossibleScore(cls, rounds: int) -> int:
        """Returns the highest possible score a player can achieve given the number of `rounds`"""
        return max(cls.TEMPTATION, cls.SUCKER, cls.REWARD, cls.PENALTY) * rounds

    @classmethod
    def lowestPossibleScore(cls, rounds: int) -> int:
        """Returns the lowest possible score a player can achieve given the number of `rounds`"""
        return min(cls.TEMPTATION, cls.SUCKER, cls.REWARD, cls.PENALTY) * rounds


def oneVersusMany(p1: Player, l2: List[Dna], rounds: int = None) -> int:
    """Makes the given player `p1` play against a list of DNAs `l2`.
    Returns the total score `p1` achieved from every opponent.
    Will use the given number of rounds if given or use the default."""
    return sum([PDGame(p1, Player.from_dna(d2), rounds)()[0].score for d2 in l2])

def manyVersusMany(l1: List[Dna], l2: List[Dna], rounds: int = None) -> Tuple[List[int],List[int]]: # Generator[Tuple[int,int], Tuple[int,int], Tuple[List[int],List[int]]]
    """Makes the given list of DNAs `l1` play against the other given list `l2`.
    Will use the given number of rounds if given or use the default.
    """
    """
    Returns
    -------
    Generator object to play all the games.
    - Returns: Pair of lists for the total scores each player obtained in total
    - Yields: Scores of each game played
    - Sends: Pair of indices of the DNAs to play against eachother
    """
    res = ([0]*len(l1), [0]*len(l2))
    for i, d1 in enumerate(l1):
        for j, d2 in enumerate(l2):
            (p1s, p2s) = PDGame(Player.from_dna(d1), Player.from_dna(d2), rounds).playAll()
            res[0][i] += p1s.score
            res[1][j] += p2s.score
            # (i, j) = yield p1s, p2s
    return res


def manyVersusOne(l1: List[Dna], p2: Player, rounds: int = None) -> List[int]:
    """Makes the given list of DNAs `l1` play against the a given player `p2`.
    Returns a list of the scores each player in `l1` scored against `p2`.
    Will use the given number rounds if given or use the default."""
    return [PDGame(Player.from_dna(d1), p2, rounds)()[0].score for d1 in l1]


def battleRoyale(l: List[Dna], rounds: int = None) -> List[int]:
    """Makes a list of DNAs play against eachother and returns the total scores of each player.
    Will use the given number of rounds if given or use the default."""
    # Play against self, once
    r = [PDGame(Player.from_dna(d), Player.from_dna(d), rounds)()[0].score for d in l]
    # Play against eachother
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            p1s, p2s = PDGame(Player.from_dna(l[i]), Player.from_dna(l[j]), rounds)()
            r[i] += p1s.score
            r[j] += p2s.score
    return r
