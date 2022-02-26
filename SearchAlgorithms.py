from struct import unpack
from typing import List
from Dna import Dna
from Player import Player
from Heuristics import *
from random import *
import math

def generateRandomStrategies(memDepth: int, nodeSize: int, n: int) -> List[Dna]:
    """Generates `n` random strategies with the given memory depth and node size"""
    N :int = nodeSize ** memDepth + memDepth
    return [Dna.from_random(N) for i in range(n)]

def getSuccessors(strat:Dna) -> List[Dna]:
    """ Returns the list of successors for a given strategy.
        Successors of a strategy `strat` are defined as the set of all strategies
        that differ by exactly one bit. Returned list will be of size `len(strat)`"""
    return [strat^(1<<i) for i in range(len(strat))]

def localBeam(memDepth: int, nodeSize: int, k: int) -> Dna:
    """TODO"""
    print("----Local Beam----")
    i = 0

    # randomly generated opponents used for manyVsMany Heuristic
    NUM_OPPONENTS = 10
    opponents = generateRandomStrategies(memDepth, nodeSize, NUM_OPPONENTS)

    stratLst = generateRandomStrategies(memDepth, nodeSize, k)

    while True:
        # finds the top performing strategy and its score
        scoreList = manyVersusMany(stratLst, opponents)
        scoreList, stratLst = zip(*sorted(zip(scoreList, stratLst)))
        topStrat = stratLst[-1]
        topScore = scoreList[-1]

        print("\ti:", i)
        print("\t\ttopScore:", topScore)

        # finds all the successors from the list of strategies
        successors = [s for S in stratLst for s in getSuccessors(S)]
        successors = [_k for _k in dict.fromkeys(successors)] # removes duplicate entries (not tested yet TODO)
        print("\t\tlen(stratLst):", len(stratLst), "  | len(successors):", len(successors))

        # calculates the scores of all successors and sorts them by score
        scoreList = manyVersusMany(successors, opponents)
        scoreList, successors = zip(*sorted(zip(scoreList, stratLst)))

        print("\t\ttopSucScore:", scoreList[-1])

        # return highest preforming strat if no better strat is found in successors
        if topScore >= scoreList[-1]:
            return topStrat

        # repeat with the k highest performing successors
        stratLst = successors[-k:]

        i += 1


def hillClimb(memDepth: int, nodeSize: int) -> Dna:
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
        scoreLst = manyVersusOne(Dna("CCDDC"), successors)
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


def simulatedAnnealing(memDepth: int, nodeSize: int) -> Dna:
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