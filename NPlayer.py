
import random



class Player:
    outcomes :dict = { v:k for k,v in enumerate("RTSP") } # factors as dictionary
    nodeSize :int = len(outcomes)

    def __init__(self, strat:str, initMoves:str):
        self.memDepth = len(initMoves)
        self.stratSize = self.nodeSize ** self.memDepth
        self.curState :str = "." * self.memDepth # Starts empty, needs initializing
        self.initMoves = initMoves
        self.strategy :str = strat
        # Can also check if strategy is valid (consists only of letters from `factors`)
        assert(self.stratSize == len(self.strategy))
        self.score :int = 0 # Player wants to maximize this

    def encodeHistory (self)->int:
        """Encodes the current state into an int from [0,`stratSize`)"""
        result :int = 0
        step : int = self.stratSize / self.nodeSize # Value of last 'bit'
        for i in range(self.memDepth):
            result += step * self.outcomes[self.curState[i]]
            step /= self.nodeSize
        return result

    def getMove (self)->str:
        """Returns whether this player would C or D for the current history and strategy"""
        if self.curState[0]=='.':
            print("Error, player was not itialized yet!")
            exit(-1)
        return self.strategy[self.encode_curState()]
    
    def updateHistory (self, outcome:str):
        """Updates the history with the oponents `newState`"""
        self.curState = self.curState[1:] + outcome
    
def initializePlayers (p1:Player, p2:Player):
    """Prepopulate the history of both given players using their initial moves"""
    p1M = len(p1.initMoves)
    p2M = len(p2.initMoves)
    M = max(p1M, p2M)
    for m in range(M):
        p1m = p1.initMoves[m] if m < p1M else p1.getMove()
        p2m = p2.initMoves[m] if m < p2M else p2.getMove()
        result = p1m + p2m
        if result == "CC":
            p1.updateHistory("R")
            p2.updateHistory("R")
        elif result == "DC":
            p1.updateHistory("T")
            p2.updateHistory("S")
        elif result == "CD":
            p1.updateHistory("S")
            p2.updateHistory("T")
        elif result == "DD":
            p1.updateHistory("P")
            p2.updateHistory("P")
        else:
            print("Error, invalid move")
            exit(-1)

    

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
