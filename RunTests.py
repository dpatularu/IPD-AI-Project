from SearchAlgorithms import *
import statistics
from tqdm import tqdm
from matplotlib import pyplot
import numpy
import pickle
from os import path
from Annealing import simulatedAnnealing
from LocalBeam import localBeam
from Genetic import genetic
from HillClimb import *

VALID_ALGOS = ["hillclimb", "localbeam", "annealing", "genetic"]
NUM_HILLCLIMB_PARAMS = 3
NUM_LOCALBEAM_PARAMS = 4
NUM_ANNEALING_PARAMS = 3
NUM_GENETIC_PARAMS = 7

ABS_DATA_PATH = "D:/School/COMP3710/ai-project/data/"
DATA_PATH = "DATA/"


def runAlgo(algo: str, args: [], iterations: int, overwrite=False, noWrite=False) -> [Dna]:
    """ Runs a local search algorithm a given number of times.
        Returns and logs the results. """

    if algo not in VALID_ALGOS:
        print("invalid alogrithm name:", algo)
        return

    fileFormat = DATA_PATH + "{algo}_{args}_{iterations}.dat"
    argsStr = str(args).replace(" ", "").replace("'", "")
    filePath = fileFormat.format(algo=algo, args=argsStr, iterations=iterations)

    if path.exists(filePath) and not overwrite:
        print("'" + filePath + "' already exists")
        readFile = open(filePath, "rb")
        data = pickle.load(readFile)
        readFile.close()
        return data

    assert len(args) >= 3, "need at least 3 parameters"

    data = []
    if algo == "hillclimb":
        assert len(args) == NUM_HILLCLIMB_PARAMS, "invalid number of parameters"
        for _ in tqdm(range(iterations)):
            data.append(hillClimb(args[0], args[1], args[2]))
    elif algo == "localbeam":
        assert len(args) == NUM_LOCALBEAM_PARAMS, "invalid number of parameters"
        for _ in tqdm(range(iterations)):
            data.append(localBeam(args[0], args[1], args[2], args[3]))
    elif algo == "annealing":
        assert len(args) == NUM_ANNEALING_PARAMS, "invalid number of parameters"
        for _ in tqdm(range(iterations)):
            data.append(simulatedAnnealing(args[0], args[1], args[2]))
    elif algo == "genetic":
        assert len(args) == NUM_GENETIC_PARAMS, "invalid number of parameters"
        for _ in tqdm(range(iterations)):
            data.append(genetic(args[0], args[1], args[2], args[3], args[4], args[5], args[6]))

    if noWrite:
        return data

    writeFile = open(filePath, 'wb')
    pickle.dump(data, writeFile)
    writeFile.close()
    return data


def playAlgos(algo1: str, args1: [], algo2: str, args2: [], iterations: int, rounds: int,
              overwrite=False, noWrite=False) -> [[int]]:
    """ Plays the results of two local search algorithms against each other.
        Returns and logs the results. """
    if algo1 not in VALID_ALGOS:
        print("invalid alogrithm names:", algo1)
        return
    elif algo2 not in VALID_ALGOS:
        print("invalid alogrithm names:", algo1)
        return

    fileFormat = DATA_PATH + "{algo}_{args}_{iterations}.dat"

    argsStr1 = str(args1).replace(" ", "").replace("'", "")
    filePath1 = fileFormat.format(algo=algo1, args=argsStr1, iterations=iterations)
    if not path.exists(filePath1) or overwrite:
        strats1 = runAlgo(algo1, args1, iterations, overwrite=True, noWrite=noWrite)
    else:
        print("'" + filePath1 + "' already exists")
        readFile = open(filePath1, "rb")
        strats1 = pickle.load(readFile)
        readFile.close()

    argsStr2 = str(args2).replace(" ", "").replace("'", "")
    filePath2 = fileFormat.format(algo=algo2, args=argsStr2, iterations=iterations)
    if not path.exists(filePath2) or overwrite:
        strats2 = runAlgo(algo2, args2, iterations, overwrite=True, noWrite=noWrite)
    else:
        print("'" + filePath2 + "' already exists")
        readFile = open(filePath2, "rb")
        strats2 = pickle.load(readFile)
        readFile.close()

    fileVsFormat = DATA_PATH + "{algo1}_{args1}_vs_{algo2}_{args2}_{rounds}_{iterations}.dat"
    filePathOut = fileVsFormat.format(algo1=algo1, args1=argsStr1, algo2=algo2, args2=argsStr2,
                                      rounds=rounds, iterations=iterations)

    if path.exists(filePathOut) and not overwrite:
        print("'" + filePathOut + "' already exists")
        readFile = open(filePathOut, "rb")
        data = pickle.load(readFile)
        readFile.close()
        return data

    scores = manyVersusMany(strats1, strats2, rounds, track=True)
    scores1 = scores[0]
    scores2 = scores[1]

    if noWrite:
        return scores1, scores2

    writeFile = open(filePathOut, 'wb')
    pickle.dump([scores1, scores2], writeFile)
    writeFile.close()

    return scores1, scores2


def compareScores(scores1: [int], label1: str, scores2: [int], label2: str):
    """ Describes and plots the scores of two strategies. """
    print(label1)
    print("\tavg:", statistics.mean(scores1))
    print("\ttop:", max(scores1))

    print(label2)
    print("\tavg:", statistics.mean(scores2))
    print("\ttop:", max(scores2))

    bins = numpy.linspace(min(min(scores1), min(scores2)), max(max(scores1), max(scores2), 100))
    pyplot.hist(scores1, bins, alpha=0.5, label=label1)
    pyplot.hist(scores2, bins, alpha=0.5, label=label2)
    pyplot.legend(loc='upper left')
    pyplot.show()


def hillClimbTests():
    shortIterations = 10
    iterations = 100
    longIterations = 1000

    algo = "hillclimb"
    memDepth = 3
    rounds = 5
    heuristic = "AMD1"

    print("hillClimb AMD1 vs HP")
    scores = playAlgos(algo, [memDepth, rounds, "AMD1"],
                       algo, [memDepth, rounds, "HP"],
                       iterations, rounds, noWrite=True)
    compareScores(scores[0], "AMD1", scores[1], "HP")
