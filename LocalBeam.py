
from Dna import Dna
from SearchAlgorithms import getNeighbors
from Generators import GenDna
from PDGame import manyVersusMany
from Player import Player

def localBeam(memDepth: int, k: int, maxRounds:int) -> Dna:
    """TODO"""
    print("----Local Beam----")
    i = 0

    # randomly generated opponents used for manyVsMany Heuristic
    NUM_OPPONENTS = 10
    opponents = GenDna.random_list(NUM_OPPONENTS, memDepth)

    stratLst = GenDna.random_list(k, memDepth)

    for i in range(maxRounds):
        # finds the top performing strategy and its score
        scoreList = manyVersusMany(stratLst, opponents)
        scoreList, stratLst = zip(*sorted(zip(scoreList, stratLst)))
        topStrat = stratLst[-1]
        topScore = scoreList[-1]

        print("\ti:", i)
        print("\t\ttopScore:", topScore)

        # finds all the successors from the list of strategies
        successors = [s for S in stratLst for s in getNeighbors(S)]
        successors = [_k for _k in dict.fromkeys(successors)]

        print("\t\tlen(stratLst):", len(stratLst), "  | len(successors):", len(successors))

        # calculates the scores of all successors and sorts them by score
        scoreList = manyVersusMany(successors, opponents)
        scoreList, successors = zip(*sorted(zip(scoreList, successors)))

        print("\t\ttopSucScore:", scoreList[-1])

        # return highest preforming strat if no better strat is found in successors
        if topScore >= scoreList[-1]:
            return topStrat

        # repeat with the k highest performing successors
        stratLst = successors[-k:]
