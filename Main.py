import random
from App import App
from PDGame import oneVersusMany
from Player import Player
from Genetic import genetic
from HillClimb import *
from SearchAlgorithms import *

def run_genetic_example():
    memDepth = 2
    popSize = 500
    mutationRate = 0.3
    generations = 200
    return genetic(memDepth, popSize, mutationRate, generations)
    # s = simulatedAnnealing(memDepth, nodeSize)
    #b = localBeam(memDepth, nodeSize, 10)
    

def run_hillClimb_example():
    memDepth = 2
    return hillClimb(memDepth)

def main():
    random.seed()

    app = App()
    
    # h = run_hillClimb_example()

    # print("Final DNA:", h)
    # l = generateSamplePopulation(2, 50000)
    # s = oneVersusMany(Player.from_dna(g), l) / 64 / len(l)
    # print("Ave Score:", s)

    return

if __name__ == "__main__":
    main()
