import random
from typing import List
from Dna import Dna
from Play import playPrisonersDillema
from Player import Player
from SearchAlgorithms import generateRandomStrategies
from Heuristics import *
    
def createNewGeneration(fitnessLst: List[int], stratLst: List[Dna], numElite: int) -> Dna:
    newGeneration = []
    for i in range(0, numElite): 
        newGeneration.append(stratLst[-(i+1)]) #Allows the best strategies to move on without alteration
    
    while len(newGeneration) < len(stratLst):
        mates = random.choices(population=stratLst, weights=fitnessLst, k=2)
        child = recombine(mates[0], mates[1])
        newGeneration.append(child)
    return newGeneration

def mutate(strat: Dna) -> Dna:
    """changes 1 random element in a given strategy"""
    return strat ^ (1 << random.randint(0, strat.size-1))


def recombine(strat1: Dna, strat2: Dna) -> Dna:
    """crosses over two strategies"""
    assert len(strat1) == len(strat2)
    if len(strat1) == 1: return random.choice([strat1, strat2]) 
    i = random.randint(0, len(strat1)-1)
    firstHalf = strat1[:i]
    secondHalf = strat2[i:]
    return firstHalf + secondHalf

def genetic(memDepth: int, nodeSize: int, popSize: int, mutationRate: float, generations: int) -> Dna:
    """Generates a strategy with given memory depth and node size by randomly generating a
    population of random strategies, playing them against each other for a given number of
    generations and assigning a fitness value for each. Subsequent generations are chosen by
    selecting members of the population with probability proportional to their fitness score.
    Each generation, every strategy has a chance to mutate given by the mutation rate.

    Parameters
    ----------
    `memDepth` : int
        The memory depth of a strategy
    `nodeSize` : int
        The base value for encoding a strategy. Either 2 if {CD} or 4 if {RTSP}
    `popSize` : int
        The size of the population. Must be even to allow for valid crossover pairings.
    `mutationRate` : float
        The probability that a strategy will mutate
    `generations` : int
        The total number of generations

    Returns
    -------
    `strategy` : (str, str)
        A tuple containing the strategy encoding and the initial moves for the highest
        performing strategy after all generations
    """
    assert popSize % 2 == 0

    # generate an initial population
    stratLst = generateRandomStrategies(memDepth, nodeSize, popSize)

    for g in range(generations):
        # sort the population by fitness
        fitnessLst = manyVersusMany(stratLst, [Dna("CCDDC")])
        fitnessLst, stratLst = zip(*sorted(zip(fitnessLst, stratLst)))

        stratLst = createNewGeneration(fitnessLst, stratLst, 2)

        # mutate the population
        for i in range(len(stratLst)):
            # chance to mutate strategy
            rand = random.random()
            if rand < mutationRate:
                stratLst[i] = (mutate(stratLst[i][0]), stratLst[i][1])
            # chance to mutate initial moves independent of strategy
            rand = random.random()
            if rand < mutationRate:
                stratLst[i] = (stratLst[i][0], mutate(stratLst[i][1]))

    # evaluate and return the highest performing strategy
    fitnessLst = manyVersusMany(stratLst, [Dna("CCDDC")])
    fitnessLst, stratLst = zip(*sorted(zip(fitnessLst, stratLst)))
    return stratLst[-1]