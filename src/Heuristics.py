from Player import Player
from Play import playPrisonersDillema
from Dna import Dna
from typing import List

NUM_ROUNDS = 64


def battleRoyale(strats: List[Dna]) -> List[int]:
    """ Takes a list of strategies that plays against each other. Returns the resulting list of scores"""
    total = 0
    fitnessLst = [0] * len(strats)
    for i in range(len(strats) - 1):
        testSubject = Player.from_dna(strats[i])
        for j in range(i + 1, len(strats)):
            competition = Player.from_dna(strats[j])
            (p1s, p2s) = playPrisonersDillema(testSubject, competition, NUM_ROUNDS)
            fitnessLst[i] += p1s
            fitnessLst[j] += p2s
            total += p1s + p2s
            testSubject.score = 0
    return fitnessLst


def manyVersusOne(standardStrat:Dna, strats: List[Dna]) -> List[int]:
    """ Receives one standard strategy that an array of strategies will play against.
        Returns the resulting list of scores. """
    standardPlayer = Player.from_dna(standardStrat)
    scoreLst = list()
    for strat in strats:
        competitor = Player.from_dna(strat)
        (p1s, p2s) = playPrisonersDillema(competitor, standardPlayer, NUM_ROUNDS)
        scoreLst.append(p1s)
        standardPlayer.score = 0
    return scoreLst


def manyVersusMany(strats: List[Dna], opponents: List[Dna]) -> List[int]:
    """ Takes a list of strategies and plays them against a list of opponents. Returns
        the resulting list of scores. """
    heuristicLst = []

    for i in range(len(strats)):
        player = Player.from_dna(strats[i])
        playerScore = 0
        for j in range(len(opponents)):
            opponent = Player.from_dna(opponents[j])
            (p1s, p2s) = playPrisonersDillema(player, opponent, NUM_ROUNDS)
            playerScore += p1s
            player.score = 0
        heuristicLst.append(playerScore)

    return heuristicLst

