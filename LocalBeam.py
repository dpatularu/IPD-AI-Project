from Dna import Dna
from SearchAlgorithms import getNeighbors
from Generators import GenDna
from PDGame import *


def localBeam(memDepth: int, rounds: int, heuristic: str, k: int) -> Dna:
    """ Generates a strategy using local beam method """
    MAX_ROUNDS = 1000

    opponents = []
    if heuristic == "HP":
        opponents = GenDna.allHandpicked()
    elif heuristic == "AMD1":
        opponents = GenDna.allFromSize(1)
    elif heuristic == "BR":
        pass
    else:
        print("invalid heuristic")
        exit(1)

    stratLst = GenDna.randomLst(k, memDepth)

    for i in range(MAX_ROUNDS):
        # finds the top performing strategy and its score
        scoreList = manyVersusMany(stratLst, opponents)
        scoreList, stratLst = zip(*sorted(zip(scoreList, stratLst)))
        topStrat = stratLst[-1]
        topScore = scoreList[-1]

        # finds all the successors from the list of strategies
        successors = [s for S in stratLst for s in getNeighbors(S)]
        successors = [_k for _k in dict.fromkeys(successors)]

        # calculates the scores of all successors and sorts them by score
        if heuristic == "BR":
            scoreList = battleRoyale(successors, rounds)
        else:
            scoreList = manyVersusMany(successors, opponents, rounds)
        scoreList, successors = zip(*sorted(zip(scoreList, successors)))

        # return highest preforming strat if no better strat is found in successors
        if topScore >= scoreList[-1]:
            return topStrat

        # repeat with the k highest performing successors
        stratLst = successors[-k:]
