
from Player import *

def test_everything ():

    p = Player(Dna("DDDD"), Dna("C"))
    assert p.memDepth == 1
    assert p.strategy == "DDDD"
    assert p.initMoves == "C"
    assert p.stratSize == 4
    assert p.curState == 0
    assert p.score == 0
    assert p.initialized is False
    assert Player.calcStratSize(2) == 16

    p = Player.from_str("CCDC", "C")
    p2 = Player.from_dna(Dna("CCDCC"))
    assert p == 8
    assert p == Dna("CCDCC")
    assert p == "CCDCC"
    assert p2 == 8
    assert p2 == "CCDCC"
    assert p == p2
    p = Player.from_dna(Dna.from_all_defect(5))
    assert p == "DDDDD"
    p = Player.from_id(1, 2)
    assert p == "CDCCC"

    try: p = Player.from_dna(Dna("CCCCCCC"))
    except AssertionError: pass
    else: raise AssertionError("Failed to error on bad DNA")

    p1 = Player.from_str("CCCC", "D")
    p2 = Player.from_str("DDDD", "C")

    initialize_players(p1, p2)
    assert p1.initMoves == "D"
    assert p2.initMoves == "C"
    assert p1.curState == 1
    assert p1.curState_str() == "T"
    assert p2.curState == 2
    assert p2.curState_str() == "S"
    assert p1.score == 0
    assert p2.score == 0
    assert p1.getMove() == "C"
    assert p2.getMove() == "D"
    p1.updateHistory("S")
    p2.updateHistory("T")
    assert p1.curState_str() == "S"
    assert p2.curState_str() == "T"
    assert p1.getMove() == "C"
    assert p2.getMove() == "D"
    p1.score += 30

    p3 = Player.from_str(Dna.from_all_defect(16), "CC")
    initialize_players(p1, p3)
    assert p1.score == 0
    assert p1.curState_str() == "R"
    assert p3.curState_str() == "RS"
    assert p1.getMove() == "C"
    assert p3.getMove() == "D"

    print("All tests SUCCEEDED!")
    return    

if __name__=="__main__": test_everything()    
