from platform import node
from typing import Any, List, Tuple
from Dna import Dna
from Player import Player, initializePlayers
from Play import playPrisonersDillema


def generateRandomStrategies(memDepth: int, nodeSize: int, n: int) -> List[Dna]:
    """Generates n random strategies with given memory depth and node size."""
    assert nodeSize == 2 or nodeSize == 4
    dnaLength :int = nodeSize**memDepth + memDepth
    return [Dna.from_random(dnaLength) for i in range(n)]

def getSuccessors(strat:Dna) -> List[Dna]:
    """ Returns the list of successors for a given strategy.
        Successors of a strategy 's' are defined as the set of all strategies
        that differ by exactly one 'bit' from 's'. """
    return [Dna(strat^(1<<n)) for n in range(strat.size)]

def fitness(strats: List[Dna]) -> List[int]:
    """takes a list of strategy tuples and returns the percentage fitness value for each"""
    NUM_ROUNDS = 64     # the number of consecutive rounds each strategy plays against every other strategy

    total = 0
    fitnessLst = [0] * len(strats)
    for i in range(len(strats) - 1):
        testSubject :Player = Player.from_dna(strats[i])
        for j in range(i + 1, len(strats)):
            competition :Player = Player(strats[j])
            (p1s, p2s) = playPrisonersDillema(testSubject, competition, NUM_ROUNDS)
            fitnessLst[i] += p1s
            fitnessLst[j] += p2s
            total += p1s + p2s
            testSubject.score = 0
    return fitnessLst


def hillClimb(memDepth: int, nodeSize: int) -> Any:
    """note two different ways to implement comparisons
    either compare against previous iteration's hiscore, or this iteration's highest score
    comparing against the current iterations high score gives a more meaningful result,
    but results in occasional infinite loops TODO
    """
    print("----Hill Climbing----")

    topStrat = generateRandomStrategies(memDepth, nodeSize, 1)[0]
    topStratScore = 0

    i = 0
    while True:
        print("\ti:", i, " | score:", topStratScore)

        # generate successors for our highest performing strategy
        successors = getSuccessors(topStrat)
        successors.append(topStrat)

        # calculate the fitness value for each successor and the top strategy
        scoreLst = fitness(successors)
        topStratScore = scoreLst[-1]    # compare against topStrat's score from this iteration
        scoreLst, stratLst = zip(*sorted(zip(scoreLst, successors)))

        print(scoreLst)

        # compare the fitness of the recently calculated top strategy against the previous one
        if scoreLst[-1] <= topStratScore:
            return topStrat
        topStrat = stratLst[-1]
        topStratScore = scoreLst[-1]

        i += 1
