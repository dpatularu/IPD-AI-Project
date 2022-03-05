"""Contains functions for performing Genetic based algorithms"""

import random
from Dna import Dna
from Generators import GenDna
from PDGame import *
from tqdm import tqdm


def createNewGeneration(fitnessLst: List[int], stratLst: List[Dna], numElite: int) -> List[Dna]:
    newGeneration = []
    totalFitnessScore = sum(fitnessLst)
    stratProbabilities = [fitness / totalFitnessScore for fitness in fitnessLst]
    for i in range(0, numElite):
        newGeneration.append(stratLst[-(i + 1)])  # Allows the best strategies to move on without alteration

    while len(newGeneration) < len(stratLst):
        mates = [selectOne(fitnessLst, stratLst) for i in range(2)]
        child = recombine(mates[0], mates[1])[0]
        newGeneration.append(child)
    return newGeneration

def selectOne(fitnessLst: List[int], stratLst: List[Dna]):
    totalFitnessScore = sum(fitnessLst)
    pick = random.uniform(0, totalFitnessScore)
    current = 0
    for i in range(len(stratLst)):
        current += fitnessLst[i]
        if current > pick:
            return stratLst[i]

def mutate(strat: Dna) -> Dna:
    """ Changes one random element in a given strategy """
    return strat ^ (1 << random.randint(0, len(strat) - 1))


def recombine(d1: Dna, d2: Dna) -> Tuple[Dna, Dna]:
    """ Randomly crosses over two strategies and returns those results """
    sz: int = len(d1)
    assert sz == len(d2)
    if sz < 3:
        return d2, d1
    N: int = (1 << sz) - 1
    m1: int = (1 << random.randint(1, sz-1)) - 1
    m2: int = m1 ^ N
    return Dna(d1 & m1 | d2 & m2, sz), Dna(d2 & m1 | d1 & m2, sz)


def genetic(memDepth: int, rounds: int, heuristic: str, popSize: int,
            mutationRate: float, generations: int, numElite: int) -> Dna:
    """ Generates a strategy using a genetic approach.

        Randomly generates a population of strategies and calculates their fitness by playing
        them against each other. Subsequent generations are chosen by selecting members of
        the population with probability proportional to their fitness score. Each generation,
        every strategy has a chance to mutate.

        Parameters
        ----------
        `memDepth`: int
            The memory depth of a strategy
        `popSize`: int
            The size of the population
        `mutationRate`: float
            The probability a strategy will mutate
        `generations`: int
            The total number of generations

        Returns
        -------
        `strategy`: Dna
            A Dna object containing the highest performing strategy after all generations
    """

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

    # generate an initial population
    stratLst = GenDna.randomLst(popSize, memDepth)

    for g in tqdm(range(generations)):
        # sort the population by fitness
        if heuristic == "RAN":
            opponents = GenDna.randomLst(100, 3)
        if heuristic == "BR":
            fitnessLst = battleRoyale(stratLst, rounds)
        else:
            fitnessLst = manyVersusMany(stratLst, opponents)[0]
        fitnessLst, stratLst = zip(*sorted(zip(fitnessLst, stratLst)))

        stratLst = createNewGeneration(fitnessLst, stratLst, numElite)

        # Mutate a random number of strats based off the `mutationRate`
        stratLst = [mutate(s) if random.random() < mutationRate else s for s in stratLst]

    # evaluate and return the highest performing strategy
    if heuristic == "RAN":
        opponents = GenDna.randomLst(100, 3)
    if heuristic == "BR":
        fitnessLst = battleRoyale(stratLst, rounds)
    else:
        fitnessLst = manyVersusMany(stratLst, opponents)[0]
    fitnessLst, stratLst = zip(*sorted(zip(fitnessLst, stratLst)))
    return stratLst[-1]