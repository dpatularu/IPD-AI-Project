from math import exp
import random
from Dna import Dna
from PDGame import battleRoyale
from Player import Player
from SearchAlgorithms import getNeighbors
from Generators import GenDna


def simulatedAnnealing(memDepth: int, population: int, maxRounds: int) -> Dna:
    """TODO"""
    print("----Simulated Annealing----")
    topStrat = GenDna.random(memDepth)
    opponents = GenDna.random_list(population, memDepth)
    print("initial string:", topStrat)
    topStratScore = 0

    temperature = 100
    for i in range(maxRounds):
        print("\ti:", i, " | strat:", topStrat, " | score:", topStratScore)
        temperature = .95 * temperature
        if temperature < 10: return topStrat

        successors = getNeighbors(topStrat)
        successors.append(topStrat)
        scoreLst = battleRoyale(successors)
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
