from Player import Player
from Generators import *
from Heuristics import *
from random import *
import math

def generateRandomStrategies(memDepth: int, nodeSize: int, n: int) -> [(str, str)]:
    """ Generates n random strategies with given memory depth and node size."""
    assert nodeSize == 2 or nodeSize == 4

    result: [(str, str)] = []
    for i in range(n):
        result.append((CD_Generator.random(nodeSize ** memDepth), CD_Generator.random(memDepth)))

    return result


def getSuccessors(strat: (str, str)) -> [(str, str)]:
    """ Returns the list of successors for a given strategy.
        Successors of a strategy 's' are defined as the set of all strategies
        that differ by exactly one 'bit' from 's'. """
    successors: [(str, str)] = []

    # flip one bit in init moves
    for i in range(len(strat[0])):
        if strat[0][i] == "C":
            successors.append((strat[0][:i] + "D" + strat[0][i + 1:], strat[1]))
        elif strat[0][i] == "D":
            successors.append((strat[0][:i] + "C" + strat[0][i + 1:], strat[1]))

    # flip one bit in init moves
    for i in range(len(strat[1])):
        if strat[1][i] == "C":
            successors.append((strat[0], strat[1][:i] + "D" + strat[1][i + 1:]))
        elif strat[1][i] == "D":
            successors.append((strat[0], strat[1][:i] + "C" + strat[1][i + 1:]))

    return successors


def hillClimb(memDepth: int, nodeSize: int) -> (str, str):
    """TODO"""
    print("----Hill Climbing----")
    NUM_OPPONENTS = 50

    opponents = generateRandomStrategies(memDepth, nodeSize, NUM_OPPONENTS)

    topStrat = generateRandomStrategies(memDepth, nodeSize, 1)[0]
    print("initial string:", topStrat)
    topStratScore = 0
    previousTopStrats = dict()

    i = 0
    while True:
        print("\ti:", i, " | score:", topStratScore)

        # generate successors for our highest performing strategy
        successors = getSuccessors(topStrat)
        successors.append(topStrat)

        # calculate the fitness value for each successor and the top strategy
        scoreLst = manyVersusOne(("CCDD", "C"), successors)
        topStratScore = scoreLst[-1]    # compare against topStrat's score from this iteration
        scoreLst, stratLst = zip(*sorted(zip(scoreLst, successors)))

        print(scoreLst)

        # compare the fitness of the recently calculated top strategy against the previous one
        if scoreLst[-1] <= topStratScore:
            return topStrat
        topStrat = stratLst[-1]
        topStratScore = scoreLst[-1]

        # to prevent infinite loops
        if topStrat in previousTopStrats:
            return topStrat

        previousTopStrats[topStrat] = topStratScore

        i += 1

def simulatedAnnealing(memDepth: int, nodeSize: int) -> (str, str):
    """TODO"""
    print("----Simulated Annealing----")
    topStrat = generateRandomStrategies(memDepth, nodeSize, 1)[0]
    NUM_OPPONENTS = 50
    opponents = generateRandomStrategies(memDepth, nodeSize, NUM_OPPONENTS)
    print("initial string:", topStrat)
    topStratScore = 0

    temperature = 100
    i = 1
    while True:
        print("\ti:", i, " | strat:", topStrat, " | score:", topStratScore)
        temperature = .95*temperature
        if temperature < 10: return topStrat

        successors = getSuccessors(topStrat)
        successors.append(topStrat)
        scoreLst = manyVersusOne(("CCDD", "C"), successors)
        topStratScore = scoreLst[-1]   

        nextIndex = randint(0, len(successors) - 2)
        delta = scoreLst[nextIndex] - topStratScore

        probabilityRoll = uniform(0, 1)
        epsilon = math.exp(delta/temperature)
        if delta > 0:
            topStrat = successors[nextIndex]
        else:
             if probabilityRoll < epsilon:
                topStrat = successors[nextIndex]

        i += 1