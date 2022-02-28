import random
from PDGame import oneVersusMany
from Player import Player
from Genetic import genetic
from SearchAlgorithms import *

def run_genetic_example():
    memDepth = 2
    popSize = 500
    mutationRate = 0.3
    generations = 200
    return genetic(memDepth, popSize, mutationRate, generations)
    # s = simulatedAnnealing(memDepth, nodeSize)
    #b = localBeam(memDepth, nodeSize, 10)
    

def run_hillclimb_example():
    memDepth = 2
    # h = hillClimb(memDepth, nodeSize)

def main():
    random.seed()
    
    g = run_genetic_example()

    print("Final DNA:", g)
    l = generateSamplePopulation(2, 50000)
    s = oneVersusMany(Player.from_dna(g), l) / 64 / len(l)
    print("Ave Score:", s)

    return

if __name__ == "__main__":
    main()
