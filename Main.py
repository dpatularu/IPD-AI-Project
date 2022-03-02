import random
from Annealing import simulatedAnnealing
from LocalBeam import localBeam
from PDGame import oneVersusMany
from Player import Player
from Genetic import genetic
from HillClimb import *
from SearchAlgorithms import *

def run_genetic_example():
    memDepth = 2
    popSize = 256
    mutationRate = 0.3
    generations = 256
    return genetic(memDepth, popSize, mutationRate, generations)
    # s = simulatedAnnealing(memDepth, nodeSize)
    #b = localBeam(memDepth, nodeSize, 10)
    

def run_hillClimb_example():
    memDepth = 2
    return hillClimb(memDepth)

def try_all ():
    maxRounds = 8
    memDepth = 2
    pop = 64
    mutRate = 0.5
    gens = 64

    d = hillClimb(memDepth, maxRounds)
    print("HillClimb Final:", d)
    d = simulatedAnnealing(memDepth, pop, maxRounds)
    print("Annealing Final:", d)
    d = localBeam(memDepth, pop, maxRounds)
    print("Local Beam Final:", d)
    d = genetic(memDepth, pop, mutRate, gens)
    print("Genetic Final:", d)
    return Dna(0, 1)
    

def main():
    random.seed()
    
    # h = run_genetic_example()
    # h = run_hillClimb_example()
    h = try_all()

    print("Final DNA:", h)

    return

if __name__ == "__main__":
    main()
