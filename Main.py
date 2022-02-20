
import random
from NPlayer import Player, initializePlayers
from Generators import *

def playPrisonersDillema(p1:Player, p2:Player, rounds:int)->tuple:
    """Players `r` rounds of the game with players `p1` and `p2`.  
        Returns the resulting score (p1Score, p2Score)"""
    outcomes = { "CC": "R","DC": "T","CD": "S","DD": "P" }
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

def main ():
    random.seed()
    p1 = Player(CD_Generator.random(16), CD_Generator.random(2))
    p2 = Player(CD_Generator.random(16), CD_Generator.random(2))
    initializePlayers(p1, p2)
    (p1s, p2s) = playPrisonersDillema(p1, p2, 1000)
    print("Player 1 strat:", p1.strategy)
    print("Player 2 strat:", p2.strategy)
    print("Player 1 score:", p1.score)
    print("Player 2 score:", p2.score)
    return

if __name__=="__main__": main()
