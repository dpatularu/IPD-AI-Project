import random
from Player import Player
from Play import playPrisonersDillema
from Genetic import genetic
from SearchAlgorithms import *


def main():
    # random.seed()

    memDepth = 3
    nodeSize = 4
    popSize = 100
    mutationRate = 0.001
    generations = 10
    g = genetic(memDepth, nodeSize, popSize, mutationRate, generations)
    # h = hillClimb(memDepth, nodeSize)
    # s = simulatedAnnealing(memDepth, nodeSize)
    #b = localBeam(memDepth, nodeSize, 10)
    print(g)

    p1 = Player.from_dna(g)
    p2 = Player.from_dna(Dna.from_random(67))  # Strategy and Initial Moves default to random
    (p1s, p2s) = playPrisonersDillema(p1, p2, 1000)
    # Strategy and Initial Moves default to random("Player 1 ID:", p1.strategy, p1.initMoves)
    print("Player 1 DNA:", p1)
    print("Player 2 DNA:", p2)
    print("Player 1 score:", p1s)
    print("Player 2 score:", p2s)
    return


if __name__ == "__main__":
    main()
