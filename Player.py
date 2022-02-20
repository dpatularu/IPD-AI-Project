
import random

random.seed()

class Player:

    memDepth :int = 1
    capacity :int = 4 ** memDepth

    def __init__(self, strat:str):
        self.strategy :str = strat
        self.opHistory :str = Player.initialState()
        self.score :int = 0 # Player wants to maximize this
        assert(len(self.opHistory) == Player.memDepth)
        assert(Player.capacity == len(self.strategy))

    def initialState () -> str:
        """Return an initial state for when the history is empty"""
        return "R" * Player.memDepth

    def encodeHistory (self)->int:
        """Encodes the current opponent history:str into an int from [0,4^memDepth)"""
        roundEncodings = { "R": 0,"T": 1,"S": 2,"P": 3 }
        result :int = 0
        for i in range(Player.memDepth):
            result += roundEncodings[self.opHistory[i]] * 4**(Player.memDepth - 1 - i)
        return result

    def getMove (self)->str:
        """Returns whether this player would C or D for the current history and strategy"""
        return self.strategy[self.encodeHistory()]
    
    def pushMove (self, move:str):
        """Updates the history with the oponents `move`"""
        self.opHistory = self.opHistory[1:] + move
    
    def gen_strat_rand ()->str:
        """Generates a random strat"""
        result : str = ""
        for i in range(Player.capacity):
            result += 'D' if random.random() >= 0.5 else 'C'
        return result    

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
            p1.pushMove("R")
            p2.pushMove("R")
        elif result == "T":
            p1.score += 5
            p2.score += 0
            p1.pushMove("T")
            p2.pushMove("S")
        elif result == "S":
            p1.score += 0
            p2.score += 5
            p1.pushMove("S")
            p2.pushMove("T")
        elif result == "P":
            p1.score += 1
            p2.score += 1
            p1.pushMove("P")
            p2.pushMove("P")
        else:
            print("Error, invalid move")
            exit(-1)
    return (p1.score, p2.score)

def main ():
    p1 = Player("DDDD")
    p2 = Player("DDDD")
    (p1s, p2s) = playPrisonersDillema(p1, p2, 3)
    print("Player 1 strat:", p1.strategy)
    print("Player 2 strat:", p2.strategy)
    print("Player 1 score:", p1.score)
    print("Player 2 score:", p2.score)
    return

if __name__=="__main__": main()

"""
function HILL_CLIMBING (problem) returns `state that is a local maxiumum`
input: `problem` (a problem)
local variables:`current` (a node)
                `neighbor` (a node)

current <-- MAKE_NODE (INITIAL_STATE[problem])
loop do
    neighbor <-- a highest valued successor of current
    if VALUE[neighbor] <= VALUE[current] then return STATE[current]
    current <-- neighbor
"""
# TABU: Keep fixed length queue of previously visited notes (tabu list)

"""
function SIMULATED_ANNEALING (problem, schedule) returns `solution state`
input: `problem` (a problem)
local vars: `current` (a node)
            `next` (a node)
            `T` (a 'temperature' controlling the prob. of downward steps)

current <-- MAKE_NODE(INITIAL_STATE[problem])
for t <-- 1 to infinity do
    T <-- schedule[t]
    if T==0 then return current
    next <-- randomly selected successor of current
    dE <-- VALUE[next] - VALUE[current]
    if dE > 0 then current <-- next
    else current <-- next only with probability exp(dE/T)
"""
