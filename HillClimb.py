
from typing import Any
from PDGame import battleRoyale
from Player import Player
from SearchAlgorithms import getNeighbors
from Generators import GenDna


def hillClimb(memDepth: int, maxRounds:int) -> Any:
    """note two different ways to implement comparisons
    either compare against previous iteration's hiscore, or this iteration's highest score
    comparing against the current iterations high score gives a more meaningful result,
    but results in occasional infinite loops TODO
    """
    print("----Hill Climbing----")

    topStrat = GenDna.random(memDepth)
    topStratScore = 0

    for i in range(maxRounds):
        print("\ti:", i, " | score:", topStratScore)

        # generate successors for our highest performing strategy
        successors = getNeighbors(topStrat)
        successors.append(topStrat)

        # calculate the fitness value for each successor and the top strategy
        scoreLst = battleRoyale(successors)
        topStratScore = scoreLst[-1]    # compare against topStrat's score from this iteration
        scoreLst, stratLst = zip(*sorted(zip(scoreLst, successors)))

        print(scoreLst)

        # compare the fitness of the recently calculated top strategy against the previous one
        if scoreLst[-1] <= topStratScore:
            return topStrat
        topStrat = stratLst[-1]
        topStratScore = scoreLst[-1]
