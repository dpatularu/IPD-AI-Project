
import random



class Player:

    def __init__(self, strat:str, initMoves:str, factors:str="RTSP"):
        self.nodeSz = len(factors)
        self.factors = { v:k for k,v in factors } # factors as dictionary
        self.memDepth = len(initMoves)
        self.stratSz = self.nodeSz ** self.memDepth
        self.curState :str = "." * self.memDepth # Starts empty, needs initializing
        self.strategy :str = strat
        # Can also check if strategy is valid (consists only of letters from `factors`)
        assert(self.stratSz == len(self.strategy))
        self.score :int = 0 # Player wants to maximize this

    def encodeHistory (self)->int:
        """Encodes the current state into an int from [0,`stratSz`)"""
        result :int = 0
        step : int = self.stratSz / self.nodeSz # Value of last 'bit'
        for i in range(self.memDepth):
            result += step * self.factors[self.curState[i]]
            step /= self.nodeSz
        return result

    def getMove (self)->str:
        """Returns whether this player would C or D for the current history and strategy"""
        return self.strategy[self.encode_curState()]
    
    def pushState (self, newState:str):
        """Updates the history with the oponents `newState`"""
        self.curState = self.curState[1:] + newState
        

    

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
