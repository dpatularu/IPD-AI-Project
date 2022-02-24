from Player import Player, initializePlayers
from Generators import *
from Play import playPrisonersDillema

NUM_ROUNDS = 64


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


def battleRoyale(strats: [(str, str)]) -> [int]:
    """ Takes a list of strategies that plays against each other. Returns the resulting list of scores"""
    total = 0
    fitnessLst = [0] * len(strats)
    for i in range(len(strats) - 1):
        (memDepth, strat, initMoves) = len(strats[i][1]), strats[i][0], strats[i][1]
        testSubject = Player(memDepth, strat, initMoves)
        for j in range(i + 1, len(strats)):
            competition = Player(len(strats[j][1]), strats[j][0], strats[j][1])
            (p1s, p2s) = playPrisonersDillema(testSubject, competition, NUM_ROUNDS)
            fitnessLst[i] += p1s
            fitnessLst[j] += p2s
            total += p1s + p2s
            testSubject.score = 0

    return fitnessLst


def manyVersusOne(standardStrat: (str, str), strats: [(str, str)]) -> [int]:
    """ Receives one standard strategy that an array of strategies will play against.
        Returns the resulting list of scores. """
    standardPlayer = Player(len(standardStrat[1]), standardStrat[0], standardStrat[1])
    scoreLst = list()
    for strat in strats:
        competitor = Player(len(strat[1]), strat[0], strat[1])
        (p1s, p2s) = playPrisonersDillema(competitor, standardPlayer, NUM_ROUNDS)
        scoreLst.append(p1s)
        standardPlayer.score = 0
    return scoreLst


def manyVersusMany(strats: [(str, str)], opponents: [(str, str)]) -> [int]:
    """ Takes a list of strategies and plays them against a list of opponents. Returns
        the resulting list of scores. """
    heuristicLst = []

    for i in range(len(strats)):
        (memDepth, strat, initMoves) = len(strats[i][1]), strats[i][0], strats[i][1]
        player = Player(memDepth, strat, initMoves)
        playerScore = 0
        for j in range(len(opponents)):
            opponent = Player(len(strats[j][1]), strats[j][0], strats[j][1])
            (p1s, p2s) = playPrisonersDillema(player, opponent, NUM_ROUNDS)
            playerScore += p1s
        heuristicLst.append(playerScore)

    return heuristicLst


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
