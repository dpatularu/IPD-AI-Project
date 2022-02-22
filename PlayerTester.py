
from Player import *

def test_player_from (p, m, s, i):
    assert p.memDepth == m
    assert p.strategy == s
    assert p.initMoves == i
    return p

def test_everything ():

    assert encode_CD("C") == 0
    assert encode_CD("D") == 1
    assert encode_CD("DCCC") == 1
    assert encode_CD("CCCD") == 8
    assert encode_CD("DDDDDDDDDDDDDDDDDD") == 262143

    p :Player = Player(1, 0, 0)
    assert p.stateMask == 3
    assert p.stratSize == 4
    assert p.strategy_str() == "CCCC"
    assert p.initMoves_str() == "C"
    assert p.curState_str() == "R"

    test_player_from(
        Player.from_str("DDDD", "D"),
        1, 15, 1
    )
    test_player_from(
        Player.from_str("CDCCCCCCCCCCCDCC", "CC"),
        2, 8194, 0
    )
    test_player_from(
        Player.from_dna("CCDCC"),
        1, 4, 0
    )
    test_player_from(
        Player.from_dna("CCCCCCCCCCCCCCDDDD"),
        2, 49152, 3
    )
    pb = test_player_from(
        Player.from_id(1, 3),
        1, 1, 1
    )
    assert pb.strategy_str() == "DCCC"
    assert pb.initMoves_str() == "D"
    p2 = test_player_from(
        Player.from_id(2, 9),
        2, 2, 1
    )
    assert p2.strategy_str() == "CDCCCCCCCCCCCCCC"
    assert p2.initMoves_str() == "DC"

    initialize_players(p, pb)
    assert p.initMoves_str() == "C"
    assert pb.initMoves_str() == "D"
    assert p.curState_str() == "S"
    assert pb.curState_str() == "T"
    assert p.score == 0
    assert pb.score == 0
    
    assert p.getMove() == "C"
    assert pb.getMove() == "C"
    p.updateHistory("R")
    pb.updateHistory("R")
    assert p.curState_str() == "R"
    assert pb.curState_str() == "R"
    assert p.getMove() == "C"
    assert pb.getMove() == "D"

    p2b = Player(2, 1, 1)
    initialize_players(p2, p2b)
    assert p2.score == 0
    assert p2b.score == 0
    assert p2.initMoves_str() == "DC"
    assert p2b.initMoves_str() == "DC"
    assert p2.curState_str() == "RP"
    assert p2b.curState_str() == "RP"
    assert p2.getMove() == "C"
    assert p2b.getMove() == "C"
    p2.updateHistory("R")
    p2b.updateHistory("R")
    assert p2.curState_str() == "RR"
    assert p2b.curState_str() == "RR"
    assert p2.getMove() == "C"
    assert p2b.getMove() == "D"

    print("All tests SUCCEEDED!")
    return    

if __name__=="__main__": test_everything()    
