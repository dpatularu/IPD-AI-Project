
import unittest
from Player import Player, initialize_players
from Dna import Dna

class PlayerTester (unittest.TestCase):
    
    def test_default (self):
        p = Player(Dna("DDDD"), Dna("C"))
        self.assertEqual(p.memDepth, 1)
        self.assertEqual(p.strategy, "DDDD")
        self.assertEqual(p.initMoves, "C")
        self.assertEqual(p.stratSize, 4)
        self.assertEqual(p.curState, 0)
        self.assertEqual(p.score, 0)
        self.assertFalse(p.initialized)
    
    def test_staticCalc (self):
        self.assertEqual(Player.calcStratSize(1), 4)
        self.assertEqual(Player.calcStratSize(2), 16)
        self.assertEqual(Player.calcStratSize(3), 64)
        self.assertEqual(Player.calcDnaSize(1), 5)
        self.assertEqual(Player.calcDnaSize(2), 18)
        self.assertEqual(Player.calcDnaSize(3), 67)
    
    def test_overloads (self):
        p1 = Player.from_str("CCDC", "C")
        self.assertEqual(p1, 8)
        self.assertEqual(p1, Dna("CCDCC"))
        self.assertEqual(p1, "CCDCC")
        p2 = Player.from_dna(Dna("CCDCC"))
        self.assertEqual(p2, 8)
        self.assertEqual(p2, "CCDCC")
        self.assertEqual(p1, p2)
        self.assertRaises(AssertionError, Player.from_dna, Dna("CCCCCCC"))
        
    def test_initializer (self):
        p1 = Player.from_str("CCCC", "D")
        p2 = Player.from_str("DDDD", "C")
        initialize_players(p1, p2)
        self.assertEqual(p1.initMoves, "D")
        self.assertEqual(p2.initMoves, "C")
        self.assertEqual(p1.curState, 1)
        self.assertEqual(p1.curState_str(), "T")
        self.assertEqual(p2.curState, 2)
        self.assertEqual(p2.curState_str(), "S")
        self.assertEqual(p1.score, 0)
        self.assertEqual(p2.score, 0)
        self.assertEqual(p1.getMove(), "C")
        self.assertEqual(p2.getMove(), "D")
        p1.updateHistory("S")
        p2.updateHistory("T")
        self.assertEqual(p1.curState_str(), "S")
        self.assertEqual(p2.curState_str(), "T")
        self.assertEqual(p1.getMove(), "C")
        self.assertEqual(p2.getMove(), "D")
        p1.score += 30
        p3 = Player.from_str("DDDDDDDDDDDDDDDD", "CC")
        initialize_players(p1, p3)
        self.assertEqual(p1.score, 0)
        self.assertEqual(p1.curState_str(), "R")
        self.assertEqual(p3.curState_str(), "RS")
        self.assertEqual(p1.getMove(), "C")
        self.assertEqual(p3.getMove(), "D") 

if __name__=="__main__": unittest.main()    
