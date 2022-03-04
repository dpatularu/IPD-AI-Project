import random
from App import App
from Annealing import simulatedAnnealing
from LocalBeam import localBeam
from PDGame import oneVersusMany
from Player import Player
from Genetic import genetic
from HillClimb import *
from SearchAlgorithms import *

import statistics
from tqdm import tqdm
from matplotlib import pyplot
import numpy
import pickle


def run_genetic_example():
    memDepth = 2
    popSize = 256
    mutationRate = 0.3
    generations = 256
    return genetic(memDepth, popSize, mutationRate, generations)
    # s = simulatedAnnealing(memDepth, nodeSize)
    # b = localBeam(memDepth, nodeSize, 10)


def try_all():
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


def generateTestData():
    maxRounds = 1000

    data: [Dna] = []

    ''' hillClimb
        memDepth = 3
        64 round games
        AMD1 heuristic (plays against all memDepth = 1 strategies)
        1000 iterations 
        COMPLETED '''
    # for _ in tqdm(range(1000)):
    #     data.append(hillClimb(3, maxRounds, "AMD1", 64))
    # writeFile = open('data/hillclimb_md3_r64_hAMD1_i1000.dat', 'wb')
    # pickle.dump(data, writeFile)
    # writeFile.close()

    ''' hillClimb
        memDepth = 3
        64 round games
        HP heuristic (plays against a handpicked list of strategies)
        1000 iterations 
        COMPLETED '''
    # for _ in tqdm(range(1000)):
    #     data.append(hillClimb(3, maxRounds, "HP", 64))
    # writeFile = open('data/hillclimb_md3_r64_hHP_i1000.dat', 'wb')
    # pickle.dump(data, writeFile)
    # writeFile.close()

    # readFile = open("data/hillclimb_md3_r64_hAMD1_i1000.dat", "rb")
    # hAMD1_lst = pickle.load(readFile)
    # readFile.close()
    # readFile = open("data/hillclimb_md3_r64_hHP_i1000.dat", "rb")
    # hHP_lst = pickle.load(readFile)
    # readFile.close()
    #
    # hAMD1_score = manyVersusMany(hAMD1_lst, hHP_lst, 64)
    # hHP_score = manyVersusMany(hHP_lst, hAMD1_lst, 64)
    #
    # writeFile = open('data/hAMD1_vs_hHP_i1000_score.dat', 'wb')
    # pickle.dump(hAMD1_score, writeFile)
    # writeFile.close()
    # writeFile = open('data/hHP_vs_hAMD1_i1000_score.dat', 'wb')
    # pickle.dump(hHP_score, writeFile)
    # writeFile.close()

    ''' hillClimb
        memDepth = 3
        64 round games
        AMD1 heuristic (plays against all memDepth = 1 strategies)
        100 iterations  '''
    for _ in tqdm(range(100)):
        data.append(hillClimb(3, maxRounds, "AMD1", 64))
    writeFile = open('data/hillclimb_md3_r64_hAMD1_i100.dat', 'wb')
    pickle.dump(data, writeFile)
    writeFile.close()

    ''' hillClimb
        memDepth = 3
        64 round games
        HP heuristic (plays against a handpicked list of strategies)
        100 iterations '''
    for _ in tqdm(range(100)):
        data.append(hillClimb(3, maxRounds, "HP", 64))
    writeFile = open('data/hillclimb_md3_r64_hHP_i100.dat', 'wb')
    pickle.dump(data, writeFile)
    writeFile.close()

    readFile = open("data/hillclimb_md3_r64_hAMD1_i100.dat", "rb")
    hAMD1_lst = pickle.load(readFile)
    readFile.close()
    readFile = open("data/hillclimb_md3_r64_hHP_i100.dat", "rb")
    hHP_lst = pickle.load(readFile)
    readFile.close()

    hAMD1_score = manyVersusMany(hAMD1_lst, hHP_lst, 64, track=True)
    hHP_score = manyVersusMany(hHP_lst, hAMD1_lst, 64, track=True)

    writeFile = open('data/hAMD1_vs_hHP_i100_score.dat', 'wb')
    pickle.dump(hAMD1_score, writeFile)
    writeFile.close()
    writeFile = open('data/hHP_vs_hAMD1_i100_score.dat', 'wb')
    pickle.dump(hHP_score, writeFile)
    writeFile.close()


def compareData():
    readFile = open("data/hAMD1_vs_hHP_i100_score.dat", "rb")
    hAMD1_score = pickle.load(readFile)
    readFile.close()
    readFile = open("data/hHP_vs_hAMD1_i100_score.dat", "rb")
    hHP_score = pickle.load(readFile)
    readFile.close()

    print("AMD1 heuristic")
    print("\tavg:", statistics.mean(hAMD1_score))
    print("\ttop:", max(hAMD1_score))

    print("HP heuristic")
    print("\tavg:", statistics.mean(hHP_score))
    print("\ttop:", max(hHP_score))

    bins = numpy.linspace(min(min(hHP_score), min(hAMD1_score)), max(max(hHP_score), max(hAMD1_score), 100))
    pyplot.hist(hAMD1_score, bins, alpha=0.5, label='all memDepth 1')
    pyplot.hist(hHP_score, bins, alpha=0.5, label='hand picked')
    pyplot.legend(loc='upper right')
    pyplot.show()


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
