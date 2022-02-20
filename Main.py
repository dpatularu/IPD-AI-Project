
import random
from Player import Player

def playPrisonersDillema(p1:Player, p2:Player, rounds:int)->tuple:
    """Players `r` rounds of the game with players `p1` and `p2`.  
        Returns the resulting score (p1Score, p2Score)"""
    outcomes = { "CC": "R","DC": "T","CD": "S","DD": "P" }
    for r in range(rounds):
        roundOutcome = p1.getMove() + p2.getMove()
        result = outcomes[roundOutcome]
        if result == "R":
            p1.score += 1
            p2.score += 1
            p1.pushMove("R")
            p2.pushMove("R")
        elif result == "T":
            p1.score += 20
            p2.score += 0
            p1.pushMove("T")
            p2.pushMove("S")
        elif result == "S":
            p1.score += 0
            p2.score += 20
            p1.pushMove("S")
            p2.pushMove("T")
        elif result == "P":
            p1.score += 10
            p2.score += 10
            p1.pushMove("P")
            p2.pushMove("P")
        else:
            print("Error, invalid move")
            exit(-1)
    return (p1.score, p2.score)

def main ():
    #random.seed()
    p1 = Player("DDDD")
    p2 = Player("DDDD")
    (p1s, p2s) = playPrisonersDillema(p1, p2, 3)
    print("Player 1 strat:", p1.strategy)
    print("Player 2 strat:", p2.strategy)
    print("Player 1 score:", p1.score)
    print("Player 2 score:", p2.score)
    return

if __name__=="__main__": main()
