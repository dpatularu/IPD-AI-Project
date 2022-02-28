
from Dna import *

def test_everything ():

    assert Dna.encode("C") == 0
    assert Dna.encode("D") == 1
    assert Dna.encode("DCCC") == 1
    assert Dna.encode("CCCD") == 8
    assert Dna.encode("DDDDDDDDDDDDDDDDDD") == 262143

    assert Dna.decode(1, 0) == "C"
    assert Dna.decode(1, 1) == "D"
    assert Dna.decode(4, 2) == "CDCC"
    assert Dna.decode(7, 7) == "DDDCCCC"
    
    d = Dna(6, 5)
    assert int(d) == 6
    assert len(d) == 5
    assert d.str == "CDDCC"
    assert str(d) == "CDDCC"
    assert d == Dna(6, 5)
    assert d == 6
    assert d == "CDDCC"
    
    assert Dna("CDDCC") == d
    assert Dna(d) == d
    assert not Dna(6) == d
    assert Dna(6) == "CDD"

    assert d[0] is False
    assert d[1] is True
    assert d[2] is True
    assert d[3] is False
    assert d[4] is False
    
    f = ~d
    assert f == "DCCDD"
    assert d | 1 == "DDDCC"
    assert d & 3 == "CDCCC"
    assert d ^ 12 == "CDCDC"
    assert d % 5 == "DCCCC"

    f.str = "CCCCC"
    assert str(f) == "CCCCC"

    assert Dna("D") > Dna("C")
    assert Dna("D") >= Dna("D")
    assert Dna("C") < Dna("D")
    assert Dna("C") <= Dna("C")
    assert Dna("D")<<1 == Dna("CD")
    assert Dna("CD")>>1 == Dna("D")

    dc = Dna.from_all_cooperate(7)
    assert dc == "CCCCCCC"
    dd = Dna.from_all_defect(7)
    assert dd == "DDDDDDD"

    dr = Dna.from_random(20)
    assert len(dr) == 20
    print("Random:", dr)
    dr = Dna.from_random(7)
    assert dr | dc == dr # a or F = a
    assert dr | dd == dd # a or T = T
    assert dr & dc == dc # a and F = F
    assert dr & dd == dr # a and T = a
    assert dr ^ dd == ~dr
    dc = Dna.from_all_cooperate(9)
    dd = Dna.from_all_defect(9)
    assert dr & dc == "CCCCCCCCC"
    assert dr | dd == "DDDDDDDDD"

    d = Dna(15, 4)
    d %= 1<<3
    assert d == "DDDC"

    print("All tests SUCCEEDED!")
    return    

if __name__=="__main__": test_everything()    
