
from PDGame import *
from Player import Player

def test_everything():
    
    p1 :Player = Player.from_str("DCCC", "D")
    p2 :Player = Player.from_str("DCDD", "C")

    g :PDGame = PDGame(p1, p2, 4)
    assert g.curRound == 1
    assert g.play() == "CD" # DC=TS
    assert g.curRound == 2 
    assert g.play() == "CC" # CD=ST
    assert g.curRound == 3
    assert next(g) == "DD" # CC=RR
    assert g.curRound == 4
    assert g.play() == "CD" # DD=PP
    assert g.curRound == 5
    try:
        g.play()
    except StopIteration:
        pass
    else:
        raise Exception("Did not stop iteration")
    
    assert PDGame(p2, p1, 4).playAll() == (14, 4)
    assert PDGame(p1, p2, 4)() == (4, 14)
    
    res = ["CD", "CC", "DD", "CD"]
    for i, r in enumerate(PDGame(p1, p2, 4)):
        assert r == res[i]
    assert p1.score == 4
    assert p2.score == 14

    l1 = [Dna("CCCCD"), Dna("CCCCC")]
    l2 = [Dna("DDDDC"), Dna("DDDDD")]

    assert manyVersusOne(l1, p2, 1) == [PDGame.SUCKER, PDGame.SUCKER]
    assert manyVersusMany(l1, l2) == [0, 0]
    assert oneVersusMany(p1, l2, rounds=1) == 0

    assert PDGame.highestPossibleScore(10) == 50
    assert PDGame.lowestPossibleScore(1000) == 0

    print("All tests SUCCEEDED!")

if __name__=="__main__":
    test_everything()
