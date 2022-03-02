
import unittest
from Dna import *

class DnaTester (unittest.TestCase):

    def setUp(self):
        self.d = Dna(6, 5)

    def test_encoding (self):
        self.assertEqual(Dna.encode("C"), 0)
        self.assertEqual(Dna.encode("D"), 1)
        self.assertEqual(Dna.encode("DCCC"), 1)
        self.assertEqual(Dna.encode("CCCD"), 8)
        self.assertEqual(Dna.encode("DDDDDDDDDDDDDDDDDD"), 262143)
    
    def test_decoding (self):
        self.assertEqual(Dna.decode(1, 0), "C")
        self.assertEqual(Dna.decode(1, 1), "D")
        self.assertEqual(Dna.decode(4, 2), "CDCC")
        self.assertEqual(Dna.decode(7, 7), "DDDCCCC")

    def test_default (self):
        self.assertEqual(int(self.d), 6)
        self.assertEqual(len(self.d), 5)
        self.assertEqual(self.d.str, "CDDCC")
        self.assertEqual(str(self.d), "CDDCC")
        self.assertEqual(self.d, Dna(6, 5))
        self.assertEqual(self.d, 6)
        self.assertEqual(self.d, "CDDCC")
    
    def test_construction (self):
        self.assertEqual(Dna("CDDCC"), self.d)
        self.assertEqual(Dna(self.d), self.d)
        self.assertNotEqual(Dna(6), self.d)
        self.assertEqual(Dna(6), "CDD")
    
    def test_bitIndexing (self):
        self.assertFalse(self.d[0])
        self.assertTrue(self.d[1])
        self.assertTrue(self.d[2])
        self.assertFalse(self.d[3])
        self.assertFalse(self.d[4])
    
    def test_operators (self):
        f = ~self.d
        self.assertEqual(f, "DCCDD")
        self.assertEqual(self.d | 1, "DDDCC")
        self.assertEqual(self.d & 3, "CDCCC")
        self.assertEqual(self.d ^ 12, "CDCDC")
        self.assertEqual(self.d % 5, "DCCCC")
        self.assertEqual(Dna("D")<<1, Dna("CD"))
        self.assertEqual(Dna("CD")>>1, Dna("D"))
        f = Dna(15, 4)
        f %= 1<<3
        self.assertEqual(f, "DDDC")
    
    def test_property_str (self):
        f = Dna(1,1)
        f.str = "CCCCC"
        self.assertEqual(str(f), "CCCCC")

    def test_comparisons (self):
        assert Dna("D") > Dna("C")
        assert Dna("D") >= Dna("D")
        assert Dna("C") < Dna("D")
        assert Dna("C") <= Dna("C")


    # dr = Dna.from_random(20)
    # self.assertEqual(len(dr), 20)
    # print("Random:", dr)
    # dr = Dna.from_random(7)
    # self.assertEqual(dr | dc, dr # a or F = a)
    # self.assertEqual(dr | dd, dd # a or T = T)
    # self.assertEqual(dr & dc, dc # a and F = F)
    # self.assertEqual(dr & dd, dr # a and T = a)
    # self.assertEqual(dr ^ dd, ~dr)
    # dc = Dna.from_all_cooperate(9)
    # dd = Dna.from_all_defect(9)
    # self.assertEqual(dr & dc, "CCCCCCCCC")
    # self.assertEqual(dr | dd, "DDDDDDDDD")

if __name__=="__main__": unittest.main()
