
import random


class Dna:
    """Stores a string of Cs and Ds, otherwise known as a bunch of bits.
    
    Is stored internally as a number. But you can pass in a string of Cs and Ds
    or use any of those 'from_<blank>' class methods.

    A 'C' is a 0, a 'D' is a 1.

    When parsing strings, the bits read left-to-right
    - So "CCDC" would be a value of 4 with a size of 4
    - And a value of 3 with a size of 4 would be "DDCC"
    """

    __slots__ = ['_val', '_size']
    def __init__(self, x:int|str, size:int=0):
        """Creates a piece of DNA. You can either pass in an integer
        and a size or a string of Cs and Ds."""
        if isinstance(x, str):
            self._val :int = Dna.encode(x)
            self._size :int = len(x)
        elif isinstance(x, Dna):
            self._val :int = x.val
            self._size :int = x.size
        elif isinstance(x, int):
            self._val :int = x
            self._size :int = size if size>0 else x.bit_length()
        else: raise ValueError(x)
        assert self._val < 1<<self._size, "Value of Dna must fit in the size"

    @property
    def val (self)->int:
        return self._val

    @val.setter
    def val (self, v:int):
        if v<0: raise ValueError
        self._val = v
        self._size = max(self._size, v.bit_length())

    @property
    def size (self)->int:
        return self._size

    @size.setter
    def size (self, s:int):
        if s<0: raise ValueError
        if s < self._size:
            self._val &= (1<<s)-1
        self._size = s

    def __int__(self) -> int: return self.val
    def __len__(self) -> int: return self.size
    def __str__(self) -> str: return Dna.decode(self.size, self.val)
    
    
    __default_sizing__ = [
        lambda x,y : max(x.size, y.size),
        lambda x,y : max(x.size, y.bit_length()),
        lambda x,y : max(x.size, len(y))
    ]
    """Helper function for __op__, default function"""

    def __op__(self, op, t, sizing=__default_sizing__):
        """Performs the given integer operation like | & ^, with LHS=self"""
        if isinstance(t, Dna):
            return Dna(op(self.val, t.val), sizing[0](self,t))
        elif isinstance(t, int):
            return Dna(op(self.val, t), sizing[1](self,t))
        elif isinstance(t, str):
            return Dna(op(self.val, Dna.encode(t)), sizing[2](self,t))
        else: raise TypeError

    def __or__  (self, t): return self.__op__(int.__or__,   t)
    def __ror__ (self, t): return self.__op__(int.__ror__,  t)
    def __and__ (self, t): return self.__op__(int.__and__,  t)
    def __rand__(self, t): return self.__op__(int.__rand__, t)
    def __xor__ (self, t): return self.__op__(int.__xor__,  t)
    def __rxor__(self, t): return self.__op__(int.__rxor__, t)

    def __mod__ (self, t): return self.__op__(int.__mod__, t, [
        lambda x,y : min(x.size, y.size),
        lambda x,y : max(x.size, (y-1).bit_length()),
        lambda x,y : max(x.size, len(y))
    ])

    def __lshift__(self, t): return self.__op__(int.__lshift__, t, [
        lambda x,y : x.size + y.val,
        lambda x,y : x.size + y,
        lambda x,y : x.size + len(y)
    ])

    def __rshift__(self, t): return self.__op__(int.__rshift__, t, [
        lambda x,y : x.size - y.val,
        lambda x,y : x.size - y,
        lambda x,y : x.size - len(y)
    ])

    def __bop__(self, op, t)->bool:
        if   isinstance(t, Dna): return op(self.val, t.val)
        elif isinstance(t, int): return op(self.val, t)
        elif isinstance(t, str): return op(self.val, Dna.encode(t))
        else: raise ValueError

    def __lt__(self, t): return self.__bop__(int.__lt__, t)
    def __le__(self, t): return self.__bop__(int.__le__, t)
    def __gt__(self, t): return self.__bop__(int.__gt__, t)
    def __ge__(self, t): return self.__bop__(int.__ge__, t)
    
    def __invert__(self): return Dna(self.val ^ ((1<<self.size)-1), self.size)
 
    def __getitem__(self, i:int)->bool:
        """Gets the `k`th bit in this integer, negative indexes are supported"""
        if i < 0: return bool((self.val >> (self.size-i)) & 1)
        else:     return bool((self.val >> i) & 1)
    
    def __eq__(self, o) -> bool:
        if isinstance(o, Dna):
            return self.val==o.val and self.size==o.size
        elif isinstance(o, int):
            return self.val==o and o.bit_length() <= self.size
        elif isinstance(o, str):
            return str(self) == o
        return False
    
    def __ne__(self, o) -> bool:
        return not self.__eq__(o)
    
    def __hash__(self) -> int:
        return hash(str(self))

    @staticmethod
    def decode (size:int, n:int)->str:
        """Decodes the given integer `n` into a string of Cs and Ds of size `size`"""
        result = bytearray(size)
        step :int = 1
        for m in range(size):
            result[m] = ord("D") if n & step else ord("C")
            step <<= 1
        return str(result, "ASCII")

    @staticmethod
    def encode (s:str)->int:
        """Encodes the CD string `s` into an integer"""
        result :int = 0
        step :int = 1
        RES :dict = {"C":False, "D":True}
        for i in range(len(s)):
            if RES[s[i]]:
                result |= step
            step <<= 1
        return result

    @classmethod
    def from_random (cls, size:int)->object:
        """Random string of length `size` of Cooperate or Defect, (C or D)"""
        return cls(random.randint(0, 1<<size-1), size)
    
    @classmethod
    def from_all_cooperate (cls, size:int)->object:
        """String of length `size` of all `C`s"""
        return cls(0, size)
    
    @classmethod
    def from_all_defect (cls, size:int)->object:
        """String of length `size` of all `D`s"""
        return cls((1<<size)-1, size)