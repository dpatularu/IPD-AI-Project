
import random
from typing import Iterator, List, Tuple
from Dna import Dna
from Player import Player
from SearchAlgorithms import coalesce

class GenPlayer:

    @staticmethod
    def random (memoryDepth:int):
        """Creates a random Player using `memoryDepth`"""
        return Player.from_dna(GenDna.random(Player.calcDnaSize(memoryDepth)))

    @staticmethod
    def tit4Tat(memDepth:int)->Player:
        """Creates a tit-for-tat player with the given memory depth"""
        return Player.from_str("CCDD"*(4**(memDepth-1)), "C"*memDepth)

    @staticmethod
    def susTit4Tat(memDepth:int)->Player:
        """Creates a tit-for-tat player that initially defects"""
        n :int = Player.calcStratSize(memDepth-1)
        return Player.from_str("CCDD"*n, "D"*memDepth)

    @staticmethod
    def mTit4Tat(memDepth:int)->Player:
        """Creates a player that tats if the opponents tits `memDepth` times"""
        s :str = "CCDD"
        for i in range(memDepth-1):
            s = "C"*(len(s)*2) + s + s
        return Player.from_str(s, "C"*memDepth)

    @staticmethod
    def grudger(memDepth:int)->Player:
        """Creates a player that initially cooperates but will always defect if the opponent defects once"""
        n :int = Player.calcStratSize(memDepth) - 1
        return Player.from_str("C"+ "D"*n, "C"*memDepth)

    @staticmethod
    def all_cooperate(memDepth:int)->Player:
        """Creates a player that always cooperates"""
        n :int = Player.calcStratSize(memDepth)
        return Player.from_str("C"*n, "C"*memDepth)
    
    @staticmethod
    def all_defect(memDepth:int)->Player:
        """Creates a player that always defects"""
        n :int = Player.calcStratSize(memDepth)
        return Player.from_str("D"*n, "D"*memDepth)

    @staticmethod
    def random_list(memDepth: int, n: int) -> List[Player]:
        """Returns `n` random strategies with the given memory depth and node size"""
        return [GenPlayer.random(memDepth) for i in range(n)]
    
    def get_random(memDepth:int, n:int) -> Iterator[Player]:
        """Returns a generator for a list of size `n` of random players of the given `memDepth`"""
        return (GenPlayer.random(memDepth) for i in range(n))
    
    def all_memDepth1()->List[Player]:
        """Returns a list of all players of memDepth 1"""
        return [Player.from_id(1, i) for i in range(32)]
    
    def get_memDepth1()->Iterator[Player]:
        """Returns a generator for all players of memDepth 1"""
        return (Player.from_id(1, i) for i in range(32))
    
    def all_handpicked(memDepth:int)->Tuple[Player]:
        """Returns a list of all handpicked strats"""
        return (
            GenPlayer.tit4Tat(memDepth),
            GenPlayer.susTit4Tat(memDepth),
            GenPlayer.grudger(memDepth),
            GenPlayer.all_cooperate(memDepth),
            GenPlayer.all_defect(memDepth),
            GenPlayer.mTit4Tat(memDepth)
        )

class GenDna:

    def __N(m:int,s:int|None):
        return s if m is None else Player.calcDnaSize(m)

    @staticmethod
    def random (memDepth:int, size:int=None)->Dna:
        """Returns a random DNA of `size` or `memDepth`"""
        N :int = GenDna.__N(memDepth, size)
        return Dna(random.randint(0, (1<<N)-1), N)
    
    @staticmethod
    def random_list (n:int, memDepth:int, size:int=None)->List[Dna]:
        """Returns a list of random DNAs of `size` or `memDepth`"""
        return [GenDna.random(memDepth, size) for i in range(n)]
    
    @staticmethod
    def gen_random (n:int, memDepth:int, size:int=None)->List[Dna]:
        """Returns a generator for random DNAs of `size` or `memDepth`"""
        return (GenDna.random(memDepth, size) for i in range(n))

    @staticmethod
    def all_cooperate (memDepth:int, size:int=None)->object:
        """String of length `size` of all `C`s"""
        return Dna(0, GenDna.__N(memDepth,size))

    @staticmethod
    def all_defect (memDepth:int, size:int=None)->object:
        """String of length `size` of all `D`s"""
        N :int = GenDna.__N(memDepth,size)
        return Dna((1<<N)-1, N)

    @staticmethod
    def all_from_size(memDepth:int, size:int=None)->List[Player]:
        """Returns a list of all possible DNAs with the given `size`.
        Warning, grows exponentially."""
        N :int = GenDna.__N(memDepth,size)
        return [Dna(i, N) for i in range(2**N)]
    