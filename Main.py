import random
from Player import Player, initializePlayers
from Generators import *

def playPrisonersDillema(p1:Player, p2:Player, rounds:int)->tuple:
    """Players `r` rounds of the game with players `p1` and `p2`.  
        Returns the resulting score (p1Score, p2Score)"""
    outcomes = { "CC": "R","DC": "T","CD": "S","DD": "P" }
    initializePlayers(p1, p2)
    for r in range(rounds):
        roundOutcome = p1.getMove() + p2.getMove()
        result = outcomes[roundOutcome]
        if result == "R":
            p1.score += 3
            p2.score += 3
            p1.updateHistory("R")
            p2.updateHistory("R")
        elif result == "T":
            p1.score += 5
            p2.score += 0
            p1.updateHistory("T")
            p2.updateHistory("S")
        elif result == "S":
            p1.score += 0
            p2.score += 5
            p1.updateHistory("S")
            p2.updateHistory("T")
        elif result == "P":
            p1.score += 1
            p2.score += 1
            p1.updateHistory("P")
            p2.updateHistory("P")
        else:
            print("Error, invalid move")
            exit(-1)
    return (p1.score, p2.score)

def play_against_everyone (p1:Player)->int:
    rounds :int = 1000
    totalScore :float = 0.0
    m : int = p1.memDepth
    p2k = 4**m + m # Length of UID
    N = 2**p2k
    for n in range(N):
        p2id = CD_Generator.from_number(p2k, n)
        p2 = Player(m, p2id[:-m], p2id[-m:])
        (p1s, p2s) = playPrisonersDillema(p1, p2, rounds)
        totalScore += p1s / rounds
    return totalScore / N



def main ():
    random.seed()
    p1 = Player(1)
    p1s = play_against_everyone(p1)
    # p2 = Player(2)
    # (p1s, p2s) = playPrisonersDillema(p1, p2, 1000)
    print("Player 1 ID:", p1.strategy, p1.initMoves)
    # print("Player 2 ID:", p2.strategy, p2.initMoves)
    print("Player 1 ave score:", p1s)
    # print("Player 2 ave score:", p2.score / 1000)
    return

if __name__=="__main__": main()
