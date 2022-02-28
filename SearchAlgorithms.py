"""Contains a bunch of generally useful functions or stuff"""

from typing import List
from Dna import Dna
from Player import Player
import random

# Function by 'glglgl'
def coalesce(*arg): return next((a for a in arg if a is not None), None)

def generateRandomStrategies(memDepth: int, n: int) -> List[Dna]:
    """Generates `n` random strategies with the given memory depth and node size"""
    N :int = Player.calcDnaSize(memDepth)
    return [Dna.from_random(N) for i in range(n)]

def generateSamplePopulation(memDepth:int, pop:float|int)->List[Dna]:
    """Generates a list of DNAs. Each DNA will be of memory depth `memDepth`.
    The random sampling will be evenly distributed throughout the population of DNAs of the given `memDepth`.
    - If `pop` is `int` : The returned list will be of size `pop`, negatives supported
    - If `pop` is `float` in `(0.0,1.0]` : The size of the returned list will be the `pop` percentage of the total population size"""
    dnaSize :int = Player.calcDnaSize(memDepth)
    totalPopSize :int = 1 << dnaSize
    N :int # Number of DNAs to generate
    if   isinstance(pop, int):
        N = pop
        if pop <= 0: N += totalPopSize
        elif pop > totalPopSize: N = totalPopSize
    elif isinstance(pop, float):
        if pop > 0.0 and pop <= 1.0:
            N = round(totalPopSize * pop)
        else: raise ValueError("`pop` is not a valid percentage")
    else: raise ValueError("`pop` is of an invalid type")
    interval :float = totalPopSize / N
    return [Dna(round(interval*(n + random.random())), dnaSize) for n in range(N)]

def getNeighbors(strat:Dna) -> List[Dna]:
    """ Returns the list of successors for a given strategy.
        Neighbors of a strategy `strat` are defined as the set of all strategies
        that differ by exactly one bit. Returned list will be of size `len(strat)`"""
    return [strat^(1<<i) for i in range(len(strat))]

