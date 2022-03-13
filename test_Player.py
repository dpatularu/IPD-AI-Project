
import unittest
from Dna import Dna
from Node import CD, RSTP
from Player import Player, initialize_players

class Class_Functions (unittest.TestCase):

    def test_stratSize (self):
        self.assertEqual(Player.calcStratSize(1), 4)
        self.assertEqual(Player.calcStratSize(2), 16)
        self.assertEqual(Player.calcStratSize(3), 64)

    def test_DnaSize (self):
        self.assertEqual(Player.calcDnaSize(1), 5)
        self.assertEqual(Player.calcDnaSize(2), 18)
        self.assertEqual(Player.calcDnaSize(3), 67)

    def test_split (self):
        (d1, d2) = Player.__split__(Dna("DDDDC"))
        self.assertEqual(d1, "DDDD")
        self.assertEqual(d2, "C")
        (d1,d2) = Player.__split__(Dna("DCDCDCDCDCDCDCDCCC"))
        self.assertEqual(d1, "DCDCDCDCDCDCDCDC")
        self.assertEqual(d2, "CC")
        (d1,d2) = Player.__split__(Dna(x=15, size=5)) # CDDDD
        self.assertEqual(d1, "CDDD")
        self.assertEqual(d2, "D")

    def test_combine (self):
        self.assertEqual(
            Player.__combine__(Dna("DDDD"), Dna("C")),
            "DDDDC")
        self.assertEqual(
            Player.__combine__(Dna("CCCCDDDDCCCCDDDD"), Dna("CC")),
            "CCCCDDDDCCCCDDDDCC"
        )

class PlayerTester (unittest.TestCase):
    
    def setUp (self):
        self.p = Player(Dna("DDDD"), Dna("C"))

    def test_default (self):
        self.assertEqual(self.p.memDepth, 1)
        self.assertEqual(self.p.strategy, "DDDD")
        self.assertEqual(self.p.initMoves, "C")
        self.assertEqual(self.p.curState, "R")
        self.assertEqual(self.p.stratSize, 4)
        self.assertEqual(self.p.score, 0)
        self.assertFalse(self.p.initialized)

    def test_casts (self):
        self.assertEqual(int(self.p), 30)
        self.assertEqual(str(self.p), "DDDDC")

    def test_op_equal (self):
        self.assertEqual(self.p, self.p) # Ditto
        self.assertEqual(self.p, Player(Dna("DDDD"), Dna("C"))) # Copy
        self.assertEqual(self.p, Dna("DDDDC")) # Equiv Dna
        self.assertEqual(self.p, "DDDDC") # Equiv Dna string
        self.assertEqual(self.p, 30) # Equiv ID

    def test_con_overloads (self):
        p = Player.from_str("CCDC", "C")
        self.assertEqual(p, "CCDCC")
        self.assertRaises(ValueError, Player.from_str, "CD", "DCDDDDD")

        p = Player.from_dna(Dna("CCDCC"))
        self.assertEqual(p, "CCDCC")
        self.assertRaises(AssertionError, Player.from_dna, Dna("CCCCCCC"))

        p = Player.from_id(memoryDepth=1, id=12)
        self.assertEqual(p, "CDDCC")
        p = Player.from_id(1, -1)
        self.assertEqual(p, "DDDDD")

    def test_initializer (self):
        p1 = Player.from_str("CCCC", "D")
        p2 = Player.from_str("DDDD", "C")
        initialize_players(p1, p2)
        self.assertEqual(p1.initMoves, CD.Defect)
        self.assertEqual(p2.initMoves, CD.Cooperate)
        self.assertEqual(p1.curState, "T")
        self.assertEqual(p2.curState, "S")
        self.assertEqual(p1.score, 0)
        self.assertEqual(p2.score, 0)
        self.assertEqual(p1.getMove(), CD.C)
        self.assertEqual(p2.getMove(), CD.D)
        p1.updateHistory(RSTP.Sucker)
        p2.updateHistory(RSTP.Tempted)
        self.assertEqual(p1.curState, "S")
        self.assertEqual(p2.curState, "T")
        self.assertEqual(p1.getMove(), CD.C)
        self.assertEqual(p2.getMove(), CD.D)
        p1.score += 30
        p3 = Player.from_str("DDDDDDDDDDDDDDDD", "CC")
        initialize_players(p1, p3) # (p1,p2) = (D, C), (C, C) = (T,R), (S,R)
        self.assertEqual(p1.score, 0, "Score should've been reset")
        self.assertEqual(p1.curState, "R")
        self.assertEqual(p3.curState, "RS")
        self.assertEqual(p1.getMove(), CD.C)
        self.assertEqual(p3.getMove(), CD.D) 

if __name__=="__main__": unittest.main()    
