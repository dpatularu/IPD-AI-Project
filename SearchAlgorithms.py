"""Contains a bunch of generally useful functions or stuff"""

from typing import Iterator, List
from Dna import Dna


# Function by 'glglgl'
def coalesce(*arg): return next((a for a in arg if a is not None), None)


def getNeighbors(strat: Dna) -> List[Dna]:
    """ Returns the list of successors for a given strategy.
        Neighbors of a strategy `strat` are defined as the set of all strategies
        that differ by exactly one bit. Returned list will be of size `len(strat)`"""
    return [strat ^ (1 << i) for i in range(len(strat))]


def genNeighbors(strat: Dna) -> Iterator[Dna]:
    """Returns a generator which yeilds DNAs that are a 1 bit difference from the given `strat`"""
    return (strat ^ (1 << i) for i in range(len(strat)))
