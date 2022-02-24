from Player import Player
from Generators import *
from Play import playPrisonersDillema

NUM_ROUNDS = 64


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
            opponent = Player(len(opponents[j][1]), opponents[j][0], opponents[j][1])
            (p1s, p2s) = playPrisonersDillema(player, opponent, NUM_ROUNDS)
            playerScore += p1s
            player.score = 0
        heuristicLst.append(playerScore)

    return heuristicLst
