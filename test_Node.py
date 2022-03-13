
import unittest
from Node import CD, RSTP

class Test_CD (unittest.TestCase):

    def test_eq (self):
        self.assertEqual(CD.Cooperate, 0)
        self.assertEqual(CD.C, 0)
        self.assertEqual(CD.Defect, 1)
        self.assertEqual(CD.D, 1)

    def test_cmp (self):
        self.assertGreater(CD.Defect, CD.Cooperate)
        self.assertGreaterEqual(CD.Cooperate, CD.C)
        self.assertGreaterEqual(CD.D, CD.Defect)
        self.assertLessEqual(CD.D, CD.D)
        self.assertLessEqual(CD.Cooperate, CD.Cooperate)
        self.assertLess(CD.C, CD.D)

    def test_bool (self):
        self.assertTrue(bool(CD.Defect))
        self.assertTrue(CD.D)
        self.assertFalse(bool(CD.C))
        self.assertFalse(CD.Cooperate)

    def test_str (self):
        self.assertEqual(str(CD.Cooperate), "C")
        self.assertEqual(str(CD.C), "C")
        self.assertEqual(str(CD.Defect), "D")
        self.assertEqual(str(CD.D), "D")

    def test_int (self):
        self.assertEqual(int(CD.Cooperate), 0)
        self.assertEqual(int(CD.C), 0)
        self.assertEqual(int(CD.Defect), 1)
        self.assertEqual(int(CD.D), 1)

    def test_size (self):
        self.assertEqual(CD.size(), 1)
        self.assertEqual(CD.Cooperate.size(), 1)
        self.assertEqual(CD.C.size(), 1)
        self.assertEqual(CD.Defect.size(), 1)
        self.assertEqual(CD.D.size(), 1)

    def test_index (self):
        r = "AB"
        self.assertEqual(r[CD.Cooperate], "A")
        self.assertEqual(r[CD.C], "A")
        self.assertEqual(r[CD.Defect], "B")
        self.assertEqual(r[CD.D], "B")
    
    def test_map (self):
        self.assertEqual(CD["C"], 0)
        self.assertEqual(CD["Cooperate"], 0)
        self.assertEqual(CD["D"], 1)
        self.assertEqual(CD["Defect"], 1)

class Test_RSTP (unittest.TestCase):

    def test_eq (self):
        self.assertEqual(RSTP.Reward, 0)
        self.assertEqual(RSTP.R, 0)
        self.assertEqual(RSTP.Sucker, 1)
        self.assertEqual(RSTP.S, 1)
        self.assertEqual(RSTP.Tempted, 2)
        self.assertEqual(RSTP.T, 2)
        self.assertEqual(RSTP.Penalty, 3)
        self.assertEqual(RSTP.P, 3)

    def test_cmp (self):
        self.assertGreater(RSTP.P, RSTP.T)
        self.assertGreater(RSTP.Penalty, RSTP.Sucker)
        self.assertGreater(RSTP.Tempted, RSTP.R)
        self.assertGreater(RSTP.S, RSTP.Reward)
        self.assertLess(RSTP.Reward, RSTP.P)
        self.assertLess(RSTP.R, RSTP.Tempted)
        self.assertLess(RSTP.Sucker, RSTP.Penalty)
        self.assertLess(RSTP.S, RSTP.T)
        self.assertGreaterEqual(RSTP.Sucker, RSTP.S)
        self.assertGreaterEqual(RSTP.P, RSTP.T)
        self.assertGreaterEqual(RSTP.P, RSTP.P)
        self.assertLessEqual(RSTP.P, RSTP.P)
        self.assertLessEqual(RSTP.S, RSTP.Tempted)
        self.assertLessEqual(RSTP.Reward, RSTP.R)

    def test_str (self):
        self.assertEqual(str(RSTP.Reward), "R")
        self.assertEqual(str(RSTP.R), "R")
        self.assertEqual(str(RSTP.Sucker), "S")
        self.assertEqual(str(RSTP.S), "S")
        self.assertEqual(str(RSTP.Tempted), "T")
        self.assertEqual(str(RSTP.T), "T")
        self.assertEqual(str(RSTP.Penalty), "P")
        self.assertEqual(str(RSTP.P), "P")

    def test_int (self):
        self.assertEqual(int(RSTP.Reward), 0)
        self.assertEqual(int(RSTP.R), 0)
        self.assertEqual(int(RSTP.Sucker), 1)
        self.assertEqual(int(RSTP.S), 1)
        self.assertEqual(int(RSTP.Tempted), 2)
        self.assertEqual(int(RSTP.T), 2)
        self.assertEqual(int(RSTP.Penalty), 3)
        self.assertEqual(int(RSTP.P), 3)

    def test_index (self):
        r = "ABCD"
        self.assertEqual(r[RSTP.Reward], "A")
        self.assertEqual(r[RSTP.R], "A")
        self.assertEqual(r[RSTP.Sucker], "B")
        self.assertEqual(r[RSTP.S], "B")
        self.assertEqual(r[RSTP.Tempted], "C")
        self.assertEqual(r[RSTP.T], "C")
        self.assertEqual(r[RSTP.Penalty], "D")
        self.assertEqual(r[RSTP.P], "D")

    def test_map (self):
        self.assertEqual(RSTP["R"], 0)
        self.assertEqual(RSTP["Reward"], 0)
        self.assertEqual(RSTP["S"], 1)
        self.assertEqual(RSTP["Sucker"], 1)
        self.assertEqual(RSTP["T"], 2)
        self.assertEqual(RSTP["Tempted"], 2)
        self.assertEqual(RSTP["P"], 3)
        self.assertEqual(RSTP["Penalty"], 3)

    def test_size (self):
        self.assertEqual(RSTP.size(), 2)
        self.assertEqual(RSTP.Reward.size(), 2)
        self.assertEqual(RSTP.S.size(), 2)
        self.assertEqual(RSTP.Tempted.size(), 2)
        self.assertEqual(RSTP.P.size(), 2)

if __name__=="__main__": unittest.main()
