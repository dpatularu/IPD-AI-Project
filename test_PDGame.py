
import unittest
from PDGame import *
from Player import Player

class PDGameTester (unittest.TestCase):

    def setUp(self):
        self.p1 :Player = Player.from_str("DCCC", "D")
        self.p2 :Player = Player.from_str("DCDD", "C")

    def test_staticCalc (self):
        self.assertEqual(PDGame.highestPossibleScore(10), PDGame.TEMPTATION*10)
        self.assertEqual(PDGame.lowestPossibleScore(1000), 0)


    def test_default (self):
        g :PDGame = PDGame(self.p1, self.p2, 4)
        self.assertEqual(g.curRound, 1)
        self.assertEqual(g.play(), "CD") # DC=TS
        self.assertEqual(g.curRound, 2 )
        self.assertEqual(g.play(), "CC") # CD=ST
        self.assertEqual(g.curRound, 3)
        self.assertEqual(next(g), "DD") # CC=RR
        self.assertEqual(g.curRound, 4)
        self.assertEqual(g.play(), "CD") # DD=PP
        self.assertEqual(g.curRound, 5)
        self.assertRaises(StopIteration, g.play)
    
    def test_iterAll (self):
        self.assertEqual(PDGame(self.p2, self.p1, 4).playAll(), (14, 4))
        self.assertEqual(PDGame(self.p1, self.p2, 4)(), (4, 14))
        self.assertListEqual(
            [r for r in PDGame(self.p1, self.p2, 4)],
            ["CD", "CC", "DD", "CD"])
        self.assertEqual(self.p1.score, 4)
        self.assertEqual(self.p2.score, 14)

    def test_multitudeVersus (self):
        l1 = [Dna("CCCCD"), Dna("CCCCC")]
        l2 = [Dna("DDDDC"), Dna("DDDDD")]
        self.assertEqual(manyVersusOne(l1, self.p2, 1), [PDGame.SUCKER, PDGame.SUCKER])
        self.assertEqual(manyVersusMany(l1, l2), [0, 0])
        self.assertEqual(oneVersusMany(self.p1, l2, 1), 0)
        self.assertEqual(oneVersusMany(self.p2, l1, rounds=1), 10)
        self.assertEqual(battleRoyale(l1, rounds=10), [60, 60])

if __name__=="__main__": unittest.main()
