from math import exp
import random
from Dna import Dna
from PDGame import *
from SearchAlgorithms import getNeighbors
from Generators import GenDna


def simulatedAnnealing(memDepth: int, rounds: int, heuristic: str) -> Dna:
    """ Generates a strategy using simulated annealing """
    MAX_ROUNDS = 1000

    opponents = []
    if heuristic == "HP":
        opponents = GenDna.allHandpicked()
    elif heuristic == "AMD1":
        opponents = GenDna.allFromSize(1)
    elif heuristic == "RAN":
        pass
    elif heuristic == "BR":
        pass
    else:
        print("invalid heuristic")
        exit(1)

    topStrat = GenDna.random(memDepth)

    temperature = 100
    for i in range(MAX_ROUNDS):
        temperature = .95 * temperature
        if temperature < 10:
            return topStrat

        successors = getNeighbors(topStrat)
        successors.append(topStrat)

        if heuristic == "RAN":
            opponents = GenDna.randomLst(100, 3)
        if heuristic == "BR":
            scoreLst = battleRoyale(successors, rounds)
        else:
            scoreLst = manyVersusMany(successors, opponents)[0]
        topStratScore = scoreLst[-1]

        nextIndex = random.randint(0, len(successors) - 2)
        delta = scoreLst[nextIndex] - topStratScore

        probabilityRoll = random.random()
        epsilon = exp(delta / temperature)
        if delta > 0:
            topStrat = successors[nextIndex]
        else:
            if probabilityRoll < epsilon:
                topStrat = successors[nextIndex]
