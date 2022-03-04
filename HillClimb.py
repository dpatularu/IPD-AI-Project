from PDGame import *
from SearchAlgorithms import getNeighbors
from Generators import *


def hillClimb(memDepth: int, rounds: int, heuristic: str) -> Dna:
    """ Generates a strategy using a hill climbing approach. """
    MAX_ROUNDS = 1000

    opponents = []
    if heuristic == "HP":
        opponents = GenDna.allHandpicked()
    elif heuristic == "AMD1":
        opponents = GenDna.allFromSize(1)
    elif heuristic == "BR":
        pass
    else:
        print("invalid heuristic")
        exit(1)

    topStrat = GenDna.random(memDepth)

    for _ in range(MAX_ROUNDS):
        # generate successors for our highest performing strategy
        successors = getNeighbors(topStrat)
        successors.append(topStrat)

        # calculate the fitness value for each successor and the top strategy
        if heuristic == "BR":
            scoreLst = battleRoyale(successors, rounds)
        else:
            scoreLst = manyVersusMany(successors, opponents, rounds)[0]
        topStratScore = scoreLst[-1]  # compare against topStrat's score from this iteration
        scoreLst, stratLst = zip(*sorted(zip(scoreLst, successors)))

        # compare the fitness of the recently calculated top strategy against the previous one
        if scoreLst[-1] <= topStratScore:
            return topStrat
        topStrat = stratLst[-1]
