from typing import Any
from PDGame import *
from Player import Player
from SearchAlgorithms import getNeighbors
from Generators import *


def hillClimb(memDepth: int, maxRounds: int, heuristic: str, rounds: int) -> Any:
    """TODO"""

    if heuristic == "HP":
        opponents = GenDna.allHandpicked()
    elif heuristic == "AMD1":
        opponents = GenDna.allFromSize(1)
    else:
        print("invalid heuristic")
        exit(1)

    topStrat = GenDna.random(memDepth)
    topStratScore = 0

    for i in range(maxRounds):

        # generate successors for our highest performing strategy
        successors = getNeighbors(topStrat)
        successors.append(topStrat)

        # calculate the fitness value for each successor and the top strategy
        scoreLst = manyVersusMany(successors, opponents, rounds)
        topStratScore = scoreLst[-1]  # compare against topStrat's score from this iteration
        scoreLst, stratLst = zip(*sorted(zip(scoreLst, successors)))

        # print(scoreLst)

        # compare the fitness of the recently calculated top strategy against the previous one
        if scoreLst[-1] <= topStratScore:
            return topStrat
        topStrat = stratLst[-1]
        topStratScore = scoreLst[-1]
