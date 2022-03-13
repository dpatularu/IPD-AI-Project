
from stat import FILE_ATTRIBUTE_NO_SCRUB_DATA
import unittest

from numpy import fabs
from Dna import *

class Static_Functions (unittest.TestCase):

    def test_encoding (self):
        self.assertEqual(Dna.encode("C"), 0)
        self.assertEqual(Dna.encode("D"), 1)
        self.assertEqual(Dna.encode("DCCC"), 8)
        self.assertEqual(Dna.encode("CCCD"), 1)
        self.assertEqual(Dna.encode("DDDDDDDDDDDDDDDDDD"), 262143)
    
    def test_decoding (self):
        self.assertEqual(Dna.decode(size=1, n=0), "C")
        self.assertEqual(Dna.decode(1, 1), "D")
        self.assertEqual(Dna.decode(4, 2), "CCDC")
        self.assertEqual(Dna.decode(7, 7), "CCCCDDD")
    
    def test_decoding4 (self):
        self.assertEqual(Dna.decode4(size=2, n=0), "R")
        self.assertEqual(Dna.decode4(2, 1), "S")
        self.assertEqual(Dna.decode4(2, 2), "T")
        self.assertEqual(Dna.decode4(2, 3), "P")
        self.assertEqual(Dna.decode4(4, 3), "RP")
        self.assertEqual(Dna.decode4(4, 5), "SS")
        self.assertEqual(Dna.decode4(6, 27), "STP") # 16 + 4(2) + 3
    
    def test_encoding4 (self):
        self.assertEqual(Dna.encode4("R"), 0)
        self.assertEqual(Dna.encode4("S"), 1)
        self.assertEqual(Dna.encode4("T"), 2)
        self.assertEqual(Dna.encode4("P"), 3)
        self.assertEqual(Dna.encode4("SRR"), 16)
        self.assertEqual(Dna.encode4("RTRP"), 35)

class Dna_Tester (unittest.TestCase):

    def setUp(self):
        self.d = Dna(x=6, size=5) # Should only be read from
        self.s = "CCDDC" # Should be equivalent to self.d

    def test_casts (self):
        self.assertEqual(int(self.d), 6)
        self.assertEqual(len(self.d), 5)
        self.assertEqual(str(self.d), self.s)
    
    def test_maxValue (self):
        self.assertEqual(self.d.maxValue, 31)
        self.assertEqual(Dna("CC").maxValue, 3)
        self.assertEqual(Dna("DCDC").maxValue, 15)
    
    def test_properties_getters (self):
        self.assertEqual(self.d.val, 6)
        self.assertEqual(self.d.size, 5)
        self.assertEqual(self.d.str, self.s)
    
    def test_value_setter (self):
        f = Dna(x=1, size=3) # CCD
        f.val = 2 # DC
        self.assertEqual(f, "CDC")
        f.val = 8 # DCCC
        self.assertEqual(f, "CCC")
        f.val = -1
        self.assertEqual(f, "DDD")
        f.val = -8
        self.assertEqual(f, "CCC")

    def test_size_setter (self):
        f = Dna(x=4, size=3) # DCC
        f.size = 4 # CDCC
        self.assertEqual(f, "CDCC")
        f.size = 2
        self.assertEqual(f, "CC")
        f.size = 3
        self.assertEqual(f, "CCC")

    def test_construction (self):
        self.assertEqual(Dna(self.s), self.d)
        self.assertEqual(Dna(self.d), self.d)
        self.assertNotEqual(Dna(6), self.d)
        self.assertEqual(Dna(6), "DDC")

    def test_indexing (self):
        self.assertEqual(self.d.getCD(0), CD.C)
        self.assertEqual(self.d.getCD(2), CD.D)
        self.assertEqual(self.d[1], CD.Cooperate)
        self.assertEqual(self.d[3], CD.Defect)
        self.assertEqual(self.d[-1], CD.C)
        self.assertEqual(self.d.getCD(-2), CD.D)
        self.assertRaises(IndexError, self.d.__getitem__, 5)
        self.assertEqual(self.d.getRSTP(0), RSTP.Reward)
        self.assertEqual(self.d.getRSTP(1), RSTP.P)
        # Negative indices for getRSTP for a CD Dna work but are nonsensical
        self.assertRaises(IndexError, self.d.getRSTP, 3)
    
    def test_counting (self):
        self.assertEqual(self.d.countCoops(), 3)
        self.assertEqual(self.d.countDefects(), 2)


class Dna_Operators (unittest.TestCase):

    def setUp (self):
        self.d :Dna = Dna(6, 5)
        self.s :str = "CCDDC"

    def test_equal (self):
        self.assertEqual(self.d, Dna(6, 5))
        self.assertEqual(self.d, Dna(self.s))
        self.assertEqual(self.d, self.s)
        self.assertEqual(self.d, 6)

    def test_complement (self):
        f = ~self.d
        self.assertEqual(f, "DDCCD")

    def test_or (self):
        self.assertEqual(self.d | Dna("D"), "CCDDD")
        self.assertEqual(self.d | Dna("DCCCCCC"), "DCCCDDC")
        self.assertEqual(self.d | 1, "CCDDD")
        self.assertEqual(self.d | (2**5), "DCCDDC")
        self.assertEqual(self.d | "D", "CCDDD")
        self.assertEqual(self.d | "DCCCCCC", "DCCCDDC")

    def test_and (self):
        self.assertEqual(self.d & Dna("DD"), "CCCDC")
        self.assertEqual(self.d & Dna("CCDDCC"), "CCCDCC")
        self.assertEqual(self.d & 3, "CCCDC")
        self.assertEqual(self.d & (2**5), "CCCCCC")
        self.assertEqual(self.d & "DD", "CCCDC")
        self.assertEqual(self.d & "CCCCCCCC", "CCCCCCCC")

    def test_xor (self):
        self.assertEqual(self.d ^ Dna("DD"), "CCDCD")
        self.assertEqual(self.d ^ Dna("DDDDDD"), "DDDCCD")
        self.assertEqual(self.d ^ 3, "CCDCD")
        self.assertEqual(self.d ^ (2**5), "DCCDDC")
        self.assertEqual(self.d ^ "DD", "CCDCD")
        self.assertEqual(self.d ^ "CCCCCCCC", "CCCCCDDC")

    def test_lshift (self):
        self.assertEqual(self.d<<"CDC", self.s + "CDC")
        self.assertEqual(self.d<<Dna(1,1), self.s + "D")
        self.assertEqual(self.d<<CD.Cooperate, self.s + "C")
        self.assertEqual(self.d<<1, self.s + "D")

    def test_rshift (self):
        self.assertEqual(self.d>>"CDC", "CDCCC")
        self.assertEqual(self.d>>Dna(1,2), "CDCCD")
        self.assertEqual(self.d>>CD.Defect, "DCCDD")
        self.assertEqual(self.d>>1, "DCCDD")        

    def test_comparisons (self):
        self.assertGreater(Dna("D"), Dna("C"))
        self.assertGreaterEqual(Dna("D"), Dna("D"))
        self.assertLess(Dna("C"), Dna("D"))
        self.assertLessEqual(Dna("C"), Dna("C"))

class Dna4_Operators (unittest.TestCase):

    def setUp (self):
        self.d :Dna4 = Dna4(x=6, size=3)
        self.s :str = "RST" # CCCDDC

    def test_equal (self):
        self.assertEqual(self.d, Dna4(6, 3))
        self.assertEqual(self.d, Dna(6, 6))
        self.assertEqual(self.d, Dna4(self.s))
        self.assertEqual(self.d, Dna("CCCDDC"))
        self.assertEqual(self.d, self.s)
        self.assertEqual(self.d, 6)

    def test_complement (self):
        f = ~self.d
        self.assertEqual(f, "PTS") # DDDCCD

    def test_or (self):
        f = self.d | Dna4("S")
        self.assertEqual(f, "RSP")
        self.assertEqual(self.d | Dna("D"), "CCCDDD")
        self.assertEqual(self.d | 1, "RSP")
        self.assertEqual(self.d | "S", "RSP")

    def test_and (self):
        self.assertEqual(self.d & Dna4("P"), "RRT") # CCCCDC
        self.assertEqual(self.d & Dna("DD"), "RRT")
        self.assertEqual(self.d & 3, "RRT")
        self.assertEqual(self.d & "P", "RRT")

    def test_xor (self):
        self.assertEqual(self.d ^ Dna4("RP"), "RSS") # CCCDCD
        self.assertEqual(self.d ^ Dna("CCDD"), "RSS")
        self.assertEqual(self.d ^ 3, "RSS")
        self.assertEqual(self.d ^ "RP", "RSS")

    def test_lshift (self): # RST
        self.assertEqual(self.d<<"P", self.s + "P")
        self.assertEqual(self.d<<Dna4(3,1), self.s + "P")
        self.assertEqual(self.d<<Dna(3,2), self.s + "P")
        self.assertEqual(self.d<<RSTP.Penalty, self.s + "P")
        self.assertEqual(self.d<<3, self.s + "P")

    def test_rshift (self):
        s = "PRS"
        self.assertEqual(self.d>>"P", s)
        self.assertEqual(self.d>>Dna4(3,1), s)
        self.assertEqual(self.d>>Dna(3,2), s)
        self.assertEqual(self.d>>RSTP.Penalty, s)
        self.assertEqual(self.d>>3, s)

    def test_comparisons (self):
        self.assertGreater(Dna4("T"), Dna4("R"))
        self.assertGreater(Dna4("TR"), Dna4("RSP"))
        self.assertGreaterEqual(Dna4("TR"), Dna4("RTR"))
        self.assertLess(Dna4("R"), Dna4("S"))
        self.assertLess(Dna4("RP"), Dna4("SR"))
        self.assertLessEqual(Dna4("RRRR"), Dna("R"))

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

class Dna4_Tester (unittest.TestCase):

    def setUp (self):
        self.d = Dna4(x=8, size=3)
        self.s = "RTR" # CCDCCC

    def test_default (self):
        """Constructors and equal operator"""
        self.assertEqual(self.d, self.d)
        self.assertEqual(Dna4(8,3), self.d)
        a = Dna4(self.s)
        self.assertEqual(a, self.d)
        self.assertEqual(8, self.d)
        self.assertEqual(self.s, self.d)
        self.assertNotEqual(Dna4(0, 1), self.d)

    def test_casts (self):
        self.assertEqual(int(self.d), 8)
        self.assertEqual(len(self.d), 6)
        self.assertEqual(str(self.d), self.s)

    def test_properties (self):
        self.assertEqual(self.d.val, 8)
        self.assertEqual(self.d.size, 6)
        self.assertEqual(self.d.str, self.s)

    def test_str_setter (self):
        f = Dna4(x=1, size=1)
        f.str = "PR"
        self.assertEqual(f, 12)
        self.assertEqual(f, "PR")
        self.assertEqual(str(f), "PR")

    def test_indexing (self):
        self.assertEqual(self.d.getCD(0), CD.C)
        self.assertEqual(self.d.getCD(2), CD.D)
        self.assertEqual(self.d[1], RSTP.T)
        self.assertEqual(self.d[2], RSTP.R)
        self.assertEqual(self.d.getCD(-1), CD.C)
        self.assertEqual(self.d[-3], RSTP.Reward)
        self.assertRaises(IndexError, self.d.__getitem__, 6)
        self.assertEqual(self.d.getRSTP(0), RSTP.Reward)
        self.assertEqual(self.d.getRSTP(1), RSTP.T)
        self.assertEqual(self.d.getRSTP(-1), RSTP.R)
        self.assertRaises(IndexError, self.d.getRSTP, 3)

    def test_counting (self):
        self.assertEqual(self.d.countCoops(), 5)
        self.assertEqual(self.d.countDefects(), 1)


if __name__=="__main__": unittest.main()
