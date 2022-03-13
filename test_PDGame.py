
import unittest
from PDGame import PDGame, manyVersusMany, manyVersusOne, oneVersusMany, battleRoyale
from Player import Player
from Dna import Dna

class PDGameTester (unittest.TestCase):

    def setUp(self):                     # RSTP
        self.p1 :Player = Player.from_str("DCCC", "D")
        self.p2 :Player = Player.from_str("DDCD", "C")

    def test_staticCalc (self):
        self.assertEqual(PDGame.highestPossibleScore(10), PDGame.TEMPTATION*10)
        self.assertEqual(PDGame.lowestPossibleScore(1000), 0)

    def test_default (self):
        g :PDGame = PDGame(self.p1, self.p2, 4)
        self.assertEqual(g.curRound, 1)     # States , Moves
        np1, np2 = g.play() # DC=T / CD=S , C / D
        self.assertIs(np1, self.p1)
        self.assertIs(np2, self.p2)
        self.assertEqual(np1.score, PDGame.SUCKER)
        self.assertEqual(np2.score, PDGame.TEMPTATION)
        self.assertEqual(g.curRound, 2)
        g.play()    # CD=S / DC=T , C / C
        self.assertEqual(g.curRound, 3)
        next(g)     # CC=R / CC=R , D / D
        self.assertEqual(g.curRound, 4)
        g.play()    # DD=P / DD=P , C / D
        self.assertEqual(g.curRound, 5)
        self.assertRaises(StopIteration, g.play)

    def test_iterAll (self):
        np1, np2 = PDGame(self.p2, self.p1, 4).playAll()
        self.assertEqual(np1.score, 14)
        self.assertEqual(np2.score, 4)
        np1, np2 = PDGame(self.p1, self.p2, 4)()
        self.assertEqual(np1.score, 4)
        self.assertEqual(np2.score, 14)
        for i, (np1, np2) in enumerate(PDGame(self.p1, self.p2, 4)):
            with self.subTest(round=i):
                pass
        self.assertEqual(self.p1.score, 4)
        self.assertEqual(self.p2.score, 14)

    def test_multitudeVersus (self): 
        l1 = [Dna("CCCCD"), Dna("CCCCC")]
        l2 = [Dna("DDDDC"), Dna("DDDDD")]

        # CCCC D , DDCD C  =>  T,S = C,D = S
        # CCCC C , DDCD C  =>  R,R = C,D = S
        self.assertEqual(manyVersusOne(l1, self.p2, 1), [PDGame.SUCKER, PDGame.SUCKER]) 

        # DDCD C , CCCC D  =>  S,T = D,C = T
        # DDCD C , CCCC C  =>  R,R = D,C = T
        self.assertEqual(oneVersusMany(self.p2, l1, 1), PDGame.TEMPTATION*2)

        # l1 is always coop, l2 is always defect, so l1 is always suckered, l2 always tempted
        # Lists are of length 2, hence `*2`
        expectedScores = (
            [PDGame.SUCKER*2, PDGame.SUCKER*2], # l1 scores
            [PDGame.TEMPTATION*2, PDGame.TEMPTATION*2], # l2 scored
        )
        self.assertEqual(manyVersusMany(l1, l2, 1), expectedScores)

        # Both are always coop, so they are always rewarded
        self.assertEqual(battleRoyale(l1, rounds=10), [PDGame.REWARD*20, PDGame.REWARD*20])

if __name__=="__main__": unittest.main()
