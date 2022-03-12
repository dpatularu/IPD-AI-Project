
from stat import FILE_ATTRIBUTE_NO_SCRUB_DATA
import unittest

from numpy import fabs
from Dna import *

class Static_Functions (unittest.TestCase):

    def test_CD (self):
        self.assertEqual(Dna.ALPH[0], "C")
        self.assertEqual(Dna.ALPH[1], "D")
        self.assertEqual(Dna.ALPH_D["C"], 0)
        self.assertEqual(Dna.ALPH_D["D"], 1)

    def test_RTSP (self):
        self.assertEqual(Dna4.ALPH[0], "R")
        self.assertEqual(Dna4.ALPH[1], "S")
        self.assertEqual(Dna4.ALPH[2], "T")
        self.assertEqual(Dna4.ALPH[3], "P")
        self.assertEqual(Dna4.ALPH_D["R"], 0)
        self.assertEqual(Dna4.ALPH_D["S"], 1)
        self.assertEqual(Dna4.ALPH_D["T"], 2)
        self.assertEqual(Dna4.ALPH_D["P"], 3)

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
        self.assertEqual(Dna4.decode4(size=2, n=0), "R")
        self.assertEqual(Dna4.decode4(2, 1), "S")
        self.assertEqual(Dna4.decode4(2, 2), "T")
        self.assertEqual(Dna4.decode4(2, 3), "P")
        self.assertEqual(Dna4.decode4(4, 3), "RP")
        self.assertEqual(Dna4.decode4(4, 5), "SS")
        self.assertEqual(Dna4.decode4(6, 27), "STP") # 16 + 4(2) + 3
    
    def test_encoding4 (self):
        self.assertEqual(Dna4.encode4("R"), 0)
        self.assertEqual(Dna4.encode4("S"), 1)
        self.assertEqual(Dna4.encode4("T"), 2)
        self.assertEqual(Dna4.encode4("P"), 3)
        self.assertEqual(Dna4.encode4("SRR"), 16)
        self.assertEqual(Dna4.encode4("RTRP"), 35)

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

    def test_bitIndexing (self):
        self.assertFalse(self.d.getBit(0))
        self.assertFalse(self.d[0])
        self.assertFalse(self.d[1])
        self.assertTrue(self.d.getBit(2))
        self.assertTrue(self.d[2])
        self.assertTrue(self.d[3])
        self.assertFalse(self.d[4])

class Operators (unittest.TestCase):

    def setUp (self):
        self.d = Dna(6, 5)

    def test_op_equal (self):
        self.assertEqual(self.d, Dna(6, 5))
        self.assertEqual(self.d, Dna("CCDDC"))
        self.assertEqual(self.d, "CCDDC")
        self.assertEqual(self.d, 6)

    def test_op_complement (self):
        f = ~self.d
        self.assertEqual(f, "DDCCD")

    def test_op_or (self):
        self.assertEqual(self.d | Dna("D"), "CCDDD")
        self.assertEqual(self.d | Dna("DCCCCCC"), "DCCCDDC")
        self.assertEqual(self.d | 1, "CCDDD")
        self.assertEqual(self.d | (2**5), "DCCDDC")
        self.assertEqual(self.d | "D", "CCDDD")
        self.assertEqual(self.d | "DCCCCCC", "DCCCDDC")

    def test_op_and (self):
        self.assertEqual(self.d & Dna("DD"), "CCCDC")
        self.assertEqual(self.d & Dna("CCDDCC"), "CCCDCC")
        self.assertEqual(self.d & 3, "CCCDC")
        self.assertEqual(self.d & (2**5), "CCCCCC")
        self.assertEqual(self.d & "DD", "CCCDC")
        self.assertEqual(self.d & "CCCCCCCC", "CCCCCCCC")

    def test_op_xor (self):
        self.assertEqual(self.d ^ Dna("DD"), "CCDCD")
        self.assertEqual(self.d ^ Dna("DDDDDD"), "DDDCCD")
        self.assertEqual(self.d ^ 3, "CCDCD")
        self.assertEqual(self.d ^ (2**5), "DCCDDC")
        self.assertEqual(self.d ^ "DD", "CCDCD")
        self.assertEqual(self.d ^ "CCCCCCCC", "CCCCCDDC")

    def test_op_shifts (self):
        self.assertEqual(Dna("D")<<1, Dna("DC"))
        self.assertEqual(Dna("CDC")<<2, "CDCCC")
        self.assertEqual(Dna("DC")>>1, Dna("D"))
        self.assertEqual(Dna("CDC")>>2, 0)

    def test_comparisons (self):
        self.assertGreater(Dna("D"), Dna("C"))
        self.assertGreaterEqual(Dna("D"), Dna("D"))
        self.assertLess(Dna("C"), Dna("D"))
        self.assertLessEqual(Dna("C"), Dna("C"))


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
        self.d = Dna4(x=8, size=3*2)
        self.s = "RTR"

    def test_default (self):
        """Constructors and equal operator"""
        self.assertEqual(self.d, self.d)
        self.assertEqual(Dna4(8,6), self.d)
        self.assertEqual(Dna4(self.s), self.d)
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
        f.str = "DC"
        self.assertEqual(f, "T")

if __name__=="__main__": unittest.main()
