"Contains two nodes, both int enums. One is CD, the other RSTP"

from enum import IntEnum

class CD (IntEnum):
    "A single bit int representing either Cooperate or Defect for 0 or 1 respectively"
    Cooperate = C = 0
    Defect    = D = 1

    def __str__(self)->str:
        return "CD"[self]

    def size(self=None)->int:
        return 1

class RSTP (IntEnum):
    "A two bit int representing either Reward, Sucker, Tempted, or Penalty for [0,3] respecitvely"
    Reward  = R = 0
    Sucker  = S = 1
    Tempted = T = 2
    Penalty = P = 3

    def __str__(self)->str:
        return "RSTP"[self]

    def size(self=None) -> int:
        return 2

Scoring = tuple[int,int,int,int]
"Mapping from a RSTP to an integer to score"
