import random
from Play import playPrisonersDillema
from Player import Player
from Generators import *

random.seed()


def mutate(strat: str) -> str:
    """changes 1 random element in a given strategy"""
    i = random.randint(0, len(strat) - 1)
    if strat[i] == "C":
        strat = strat[:i] + "D" + strat[i + 1:]
    else:
        strat = strat[:i] + "C" + strat[i + 1:]
    return strat


def recombine(strat1: str, strat2: str) -> (str, str):
    """crosses over two strategies"""
    assert len(strat1) == len(strat2)
    i = random.randint(1, len(strat1) - 1)
    return strat1[:i] + strat2[i:], strat2[:i] + strat1[i:]


def generateRandomStrategies(memDepth: int, base: int, n: int) -> [(str, str)]:
    """generates n random strategies with given memory depth and node size"""
    assert base == 2 or base == 4

    result: [(str, str)] = []
    for i in range(n):
        result.append((CD_Generator.random(base ** memDepth), CD_Generator.random(memDepth)))

    return result


def fitness(p1: Player, players: [Player]) -> int:
    """plays a strategy against all members in a given list and returns
    the total score"""
    NUM_ROUNDS = 64  # the number of rounds p1 plays against each opponent
    score = 0

    for player in players:
        (p1s, p2s) = playPrisonersDillema(p1, player, NUM_ROUNDS)
        score += p1s

    return score


def genPercentFitness(strats: [(str, str)]) -> [float]:
    """takes a list of strategy tuples and returns the percentage fitness value for each"""
    players = []
    for strat in strats:
        players.append(Player(len(strat[1]), strat[0], strat[1]))

    total = 0
    fitnessLst = []
    for i in range(len(players)):
        f = fitness(players[i], players[:i] + players[i + 1:])
        total += f
        fitnessLst.append(f)

    for i in range(len(fitnessLst)):
        fitnessLst[i] = fitnessLst[i] / float(total)

    return fitnessLst


def selectStrategy(fitnessLst: [float], stratLst: [(str, str)]) -> (str, str):
    """selects a strategy from a list of strategies with probability proportional to its
     percent fitness value"""
    rand = random.random()

    temp = 0
    for i in range(len(fitnessLst) - 1):
        if rand < fitnessLst[i] + temp:
            return stratLst[i]
        temp += fitnessLst[i]

    return stratLst[-1]


def genetic(memDepth: int, nodeSize: int, popSize: int, mutationRate: float, generations: int) -> (str, str):
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
        The size of each generation. Must be even to allow for valid crossover pairings.
    `mutationRate` : float
        The probability that a strategy will mutate
    `generations` : int
        The total number of generations

    Returns
    -------
    `strategy` : (str, str)
        A tuple containing the strategy encoding  and the initial moves for the highest
        performing strategy after all generations
    """
    assert popSize % 2 == 0

    # generate an initial population
    stratLst = generateRandomStrategies(memDepth, nodeSize, popSize)

    for g in range(generations):
        print("Generation:", g + 1, "/", generations)

        # sort the population by fitness
        fitnessLst = genPercentFitness(stratLst)
        fitnessLst, stratLst = zip(*sorted(zip(fitnessLst, stratLst)))

        # select a new population with each strategy having a probability
        newStratLst: (str, str) = []
        for i in range(len(stratLst)):
            newStratLst.append(selectStrategy(fitnessLst, stratLst))

        # recombine each member of the population with another
        i = 0
        stratLst: (str, str) = []
        while i < len(newStratLst):
            newStrats = recombine(newStratLst[i][0], newStratLst[i + 1][0])
            stratLst.append((newStrats[0], newStratLst[i][1]))
            stratLst.append((newStrats[1], newStratLst[i + 1][1]))
            i = i + 2

        # mutate the population
        for i in range(len(stratLst)):
            rand = random.random()
            if rand < mutationRate:
                stratLst[i] = (mutate(stratLst[i][0]), stratLst[i][1])
            elif rand < mutationRate * 2:
                stratLst[i] = (stratLst[i][0], mutate(stratLst[i][1]))

    # evaluate and return the highest performing strategy
    fitnessLst = genPercentFitness(stratLst)
    fitnessLst, stratLst = zip(*sorted(zip(fitnessLst, stratLst)))
    return stratLst[-1]