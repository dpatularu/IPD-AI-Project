
import random

random.seed()

class Player:
    memDepth :int = 6
    capacity :int = 2 ** memDepth

    def __init__(self, strat:str):
        self.strategy :str = strat
        self.opHistory :str = Player.initialState()
        self.jailTime :int = 0 # Player wants to minimize this
        assert(len(self.opHistory) == Player.memDepth)
        assert(Player.capacity == len(self.strategy))

    def initialState () -> str:
        """Return an initial state for when the history is empty"""
        return "C" * Player.memDepth

    def encodeHistory (self)->int:
        """Encodes the current opponent history:str into an int from [0,2^memDepth)"""
        result :int = 0
        l :int = Player.memDepth - 1
        for i in range(Player.memDepth):
            if self.opHistory[l-i]=="D":
                result += 2**i
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
    for r in range(rounds):
        p1m = p1.getMove()
        p2m = p2.getMove()
        result = p1m + p2m
        if result == "CC":
            p1.jailTime += 1
            p2.jailTime += 1
        elif result == "CD":
            p1.jailTime += 20
            # p2 += 0
        elif result == "DC":
            # p1 += 0
            p2.jailTime += 20
        elif result == "DD":
            p1.jailTime += 10
            p2.jailTime += 10
        else:
            print("Error, invalid move")
            exit(-1)
        p1.pushMove(p2m)
        p2.pushMove(p1m)
    return (p1.jailTime, p2.jailTime)

def main ():
    p1 = Player(Player.gen_strat_rand())
    p2 = Player(Player.gen_strat_rand())
    (p1s, p2s) = playPrisonersDillema(p1, p2, 1000000)
    print("Player 1 strat:", p1.strategy)
    print("Player 2 strat:", p2.strategy)
    print("Player 1 score:", p1s)
    print("Player 2 score:", p2s)
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
