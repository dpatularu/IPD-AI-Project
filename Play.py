from Player import Player, initializePlayers


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
