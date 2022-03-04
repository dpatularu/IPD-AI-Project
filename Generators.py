import random
from typing import Iterator, List, Tuple
from Dna import Dna
from Player import Player
from SearchAlgorithms import coalesce


class GenPlayer:

    @staticmethod
    def random(memoryDepth: int):
        """Creates a random Player using `memoryDepth`"""
        return Player.from_dna(GenDna.random(memoryDepth))

    @staticmethod
    def tit4Tat(memDepth: int) -> Player:
        """Creates a tit-for-tat player with the given memory depth"""
        return Player.from_str("CCDD" * (4 ** (memDepth - 1)), "C" * memDepth)

    @staticmethod
    def susTit4Tat(memDepth: int) -> Player:
        """Creates a tit-for-tat player that initially defects"""
        n: int = Player.calcStratSize(memDepth - 1)
        return Player.from_str("CCDD" * n, "D" * memDepth)

    @staticmethod
    def mTit4Tat(memDepth: int) -> Player:
        """Creates a player that tats if the opponents tits `memDepth` times"""
        s: str = "CCDD"
        for i in range(memDepth - 1):
            s = "C" * (len(s) * 2) + s + s
        return Player.from_str(s, "C" * memDepth)

    @staticmethod
    def grudger(memDepth: int) -> Player:
        """Creates a player that initially cooperates but will always defect if the opponent defects once"""
        n: int = Player.calcStratSize(memDepth) - 1
        return Player.from_str("C" + "D" * n, "C" * memDepth)

    @staticmethod
    def all_cooperate(memDepth: int) -> Player:
        """Creates a player that always cooperates"""
        n: int = Player.calcStratSize(memDepth)
        return Player.from_str("C" * n, "C" * memDepth)

    @staticmethod
    def all_defect(memDepth: int) -> Player:
        """Creates a player that always defects"""
        n: int = Player.calcStratSize(memDepth)
        return Player.from_str("D" * n, "D" * memDepth)

    @staticmethod
    def random_list(memDepth: int, n: int) -> List[Player]:
        """Returns `n` random strategies with the given memory depth and node size"""
        return [GenPlayer.random(memDepth) for i in range(n)]

    @staticmethod
    def get_random(memDepth: int, n: int) -> Iterator[Player]:
        """Returns a generator for a list of size `n` of random players of the given `memDepth`"""
        return (GenPlayer.random(memDepth) for i in range(n))

    @staticmethod
    def all_memDepth1() -> List[Player]:
        """Returns a list of all players of memDepth 1"""
        return [Player.from_id(1, i) for i in range(32)]

    @staticmethod
    def get_memDepth1() -> Iterator[Player]:
        """Returns a generator for all players of memDepth 1"""
        return (Player.from_id(1, i) for i in range(32))

    @staticmethod
    def all_handpicked(memDepth: int) -> List[Player]:
        """Returns a list of all handpicked strats"""
        return [
            GenPlayer.tit4Tat(memDepth),
            GenPlayer.susTit4Tat(memDepth),
            GenPlayer.grudger(memDepth),
            GenPlayer.all_cooperate(memDepth),
            GenPlayer.all_defect(memDepth),
            GenPlayer.mTit4Tat(memDepth)
        ]


class GenDna:

    def __N(m: int, s: int | None):
        return s if m is None else Player.calcDnaSize(m)

    @staticmethod
    def random(memDepth: int, size: int = None) -> Dna:
        """Returns a random DNA of `size` or `memDepth`"""
        N: int = GenDna.__N(memDepth, size)
        return Dna(random.randint(0, (1 << N) - 1), N)

    @staticmethod
    def randomLst(n: int, memDepth: int, size: int = None) -> List[Dna]:
        """Returns a list of random DNAs of `size` or `memDepth`"""
        return [GenDna.random(memDepth, size) for i in range(n)]

    @staticmethod
    def genRandom(n: int, memDepth: int, size: int = None) -> List[Dna]:
        """Returns a generator for random DNAs of `size` or `memDepth`"""
        return (GenDna.random(memDepth, size) for i in range(n))

    @staticmethod
    def allCoop() -> Dna:
        """ Returns strategy that always cooperates. """
        return Dna("CCCCC")

    @staticmethod
    def allDef() -> Dna:
        """ Returns strategy that always defects. """
        return Dna("DDDDD")

    @staticmethod
    def tit4Tat() -> Dna:
        """ Returns tit for tat strategy.
            Copies opponent's last move. Cooperates on first move. """
        return Dna("CCDDC")

    @staticmethod
    def susTit4Tat() -> Dna:
        """ Returns suspicious tit for tat strategy.
            Copies opponent's last move. Defects on first move."""
        return Dna("CCDDD")

    @staticmethod
    def twoTit4Tat() -> Dna:
        """ Returns two tit for tat strategy.
            Cooperates unless opponent defected twice in a row in previous two turns.
            Cooperates on first two moves. """
        return Dna("CCCCCCCCCCDDCCDDCC")

    @staticmethod
    def grudger() -> Dna:
        """ Returns grudger strategy.
            Cooperates until opponent defects, then only defects. """
        return Dna("CDDDC")

    @staticmethod
    def allFromSize(memDepth: int, size: int = None) -> List[Dna]:
        """Returns a list of all possible DNAs with the given `size`.
        Warning, grows exponentially."""
        N: int = GenDna.__N(memDepth, size)
        return [Dna(i, N) for i in range(2 ** N)]

    @staticmethod
    def allHandpicked() -> List[Dna]:
        """Returns a list of all handpicked strats"""
        return [
            GenDna.tit4Tat(),
            GenDna.susTit4Tat(),
            GenDna.grudger(),
            GenDna.allCoop(),
            GenDna.allDef(),
            GenDna.twoTit4Tat()
        ]
