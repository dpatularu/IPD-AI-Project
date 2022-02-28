
from math import exp
import random
from Dna import Dna
from PDGame import battleRoyale
from Player import Player
from SearchAlgorithms import generateRandomStrategies, getNeighbors

def simulatedAnnealing(memDepth: int, population:int) -> Dna:
    """TODO"""
    print("----Simulated Annealing----")
    topStrat = Player.from_random(memDepth)
    opponents = generateRandomStrategies(memDepth, population)
    print("initial string:", topStrat)
    topStratScore = 0

    temperature = 100
    i = 1
    while True:
        print("\ti:", i, " | strat:", topStrat, " | score:", topStratScore)
        temperature = .95*temperature
        if temperature < 10: return topStrat

        successors = getNeighbors(topStrat)
        successors.append(topStrat)
        scoreLst = battleRoyale(successors)
        topStratScore = scoreLst[-1]   

        nextIndex = random.randint(0, len(successors) - 2)
        delta = scoreLst[nextIndex] - topStratScore

        probabilityRoll = random.random()
        epsilon = exp(delta/temperature)
        if delta > 0:
            topStrat = successors[nextIndex]
        else:
             if probabilityRoll < epsilon:
                topStrat = successors[nextIndex]

        i += 1
