"""Contains the 'CD' Dna class"""


from functools import reduce, singledispatch
from typing import overload


class Dna:
    """Stores a string of Cs and Ds, otherwise known as a bunch of bits.
    
    Is stored internally as a number. But you can pass in a string of Cs and Ds
    or use any of those 'from_<blank>' class methods.

    A 'C' is a 0, a 'D' is a 1.

    When parsing strings, the bits read left-to-right
    - So "CCDC" would be a value of 4 with a size of 4
    - And a value of 3 with a size of 4 would be "DDCC"
    """

    ALPH :str = "CD"
    "All possible letters used by a DNA. Index this when converting int->char"

    ALPH_D :dict = {"C":False, "D":True}
    """Returns a boolean based the given letter. 'C'->F, 'D'->T"""

    NODESIZE :int = len(ALPH)
    "Number of possible letters a DNA can use. 1 past largest integer repr."

    NODEDEPTH :int = NODESIZE.bit_length()-1 # Log2(NODESIZE)
    "Number of bits required to store one letter of a DNA"

    __slots__ = ['_val', '_size']
    def __init__(self, x: int | str, size: int = 0): #TODO: Dispatch init?
        """Creates a piece of DNA. You can either pass in an integer
        and a size or a string of Cs and Ds."""
        if isinstance(x, str):
            self.str = x
        elif isinstance(x, Dna):
            self._val :int = x.val
            self._size :int = x.size
        elif isinstance(x, int):
            self._val: int = x
            self._size: int = size if size > 0 else x.bit_length()
        else: raise TypeError(x)
        self.size = self._size # Verify using setter
        self.val = self._val   # Verify using setter

    @property
    def maxValue (self)->int:
        """Returns the largest possible value for this Dna object"""
        return 2 ** self.size - 1

    @property
    def val(self) -> int:
        return self._val

    @val.setter
    def val(self, v: int):
        if v < 0: v += self.maxValue+1
        else: v &= self.maxValue
        self._val = v

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, s: int):
        if s < 0: raise ValueError("DNA cannot be assigned a negative size:", s)
        self._size = s
        self._val &= self.maxValue

    @property
    def str(self) -> str:
        return Dna.decode(self.size, self.val)

    @str.setter
    def str(self, s: str):
        self._val = Dna.encode(s)
        self._size = len(s)

    def __str__(self) -> str:
        return self.str

    def __int__(self) -> int:
        return self.val

    def __len__(self) -> int:
        return self.size

    __default_sizing__ = (
        lambda x, y: max(x.size, y.size),
        lambda x, y: max(x.size, y.bit_length()),
        lambda x, y: max(x.size, len(y))
    )
    """Helper tuple for __op__, default function"""

    def __op__(self, op, t, sizing=__default_sizing__):
        """Performs the given integer operation like | & ^, with LHS=self"""
        if isinstance(t, Dna):
            return Dna(op(self.val, t.val), sizing[0](self, t))
        elif isinstance(t, int):
            return Dna(op(self.val, t), sizing[1](self, t))
        elif isinstance(t, str):
            return Dna(op(self.val, Dna.encode(t)), sizing[2](self, t))
        else: raise TypeError

    def __or__  (self, t): return self.__op__(int.__or__,   t)
    def __ror__ (self, t): return self.__op__(int.__ror__,  t)
    def __and__ (self, t): return self.__op__(int.__and__,  t)
    def __rand__(self, t): return self.__op__(int.__rand__, t)
    def __xor__ (self, t): return self.__op__(int.__xor__,  t)
    def __rxor__(self, t): return self.__op__(int.__rxor__, t)

    def __lshift__(self, t):
        return self.__op__(int.__lshift__, t, [
            lambda x, y: x.size + y.val,
            lambda x, y: x.size + y,
            lambda x, y: x.size + len(y)
        ])

    def __rshift__(self, t):
        return self.__op__(int.__rshift__, t, [
            lambda x, y: x.size - y.val,
            lambda x, y: x.size - y,
            lambda x, y: x.size - len(y)
        ])

    def __bop__(self, op, t) -> bool:
        if isinstance(t, Dna):
            return op(self.val, t.val)
        elif isinstance(t, int):
            return op(self.val, t)
        elif isinstance(t, str):
            return op(self.val, Dna.encode(t))
        else: raise ValueError

    def __lt__(self, t): return self.__bop__(int.__lt__, t)
    def __le__(self, t): return self.__bop__(int.__le__, t)
    def __gt__(self, t): return self.__bop__(int.__gt__, t)
    def __ge__(self, t): return self.__bop__(int.__ge__, t)

    def __invert__(self):
        return Dna(self.val ^ (2**self.size - 1), self.size)

    def getBit (self, i:int) -> bool:
        """Gets the `k`th bit in this integer. Negative indexes or slices not supported"""
        if i >= self.size: raise IndexError
        return bool((self.val >> (self.size - i - 1)) & 1)
    __getitem__ = getBit

    def __eq__(self, o) -> bool:
        if isinstance(o, Dna):
            return self.val == o.val and self.size == o.size
        elif isinstance(o, int):
            return self.val == o and o.bit_length() <= self.size
        elif isinstance(o, str):
            return str(self) == o
        return False

    def __ne__(self, o) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return hash(str(self))

    @staticmethod
    def decode(size: int, n: int) -> str:
        """Decodes the given integer `n` into a string of Cs and Ds of `size`"""
        return ''.join(Dna.ALPH[n >> (size-1-m) & 1] for m in range(size))

    @staticmethod
    def encode(s: str) -> int:
        """Encodes the CD string `s` into an integer"""
        step: int = 2**(len(s)-1)
        gen = ((step >> i) for i in range(len(s)) if Dna.ALPH_D[s[i]])
        return reduce(int.__or__, gen, 0)

#================================================================================================================================

class Dna4 (Dna):
    """Subclass of Dna, uses RSTP instead of CD"""

    ALPH :str = "RSTP"
    """All possible letters used by a DNA. Index this when converting int->char
    - R S T P
    - 0 1 2 3
    - b00 b01 b10 b11
    - CC CD DC DD"""

    ALPH_D :dict = {v:i for i,v in enumerate(ALPH)}
    """Converts a letter from Dna4.ALPH to it's integer representation"""

    NODESIZE :int = len(ALPH)
    "Number of possible letters a DNA can use. 1 past largest integer repr"

    NODEDEPTH :int = NODESIZE.bit_length()-1 # Log2(NODESIZE)
    "Number of bits required to store one letter of a DNA"

    def __init__(self, x: int | str, size: int = 0):
        super().__init__(x, size)

    @property
    def str(self)->str:
        return Dna4.decode4(self.size, self.val)

    @str.setter
    def str(self, s: str):
        if s[0]=="C" or s[0]=="D":
            super(Dna4, type(self)).str.fset(self, s) # Use parent setter
        else:
            self._val = Dna4.encode4(s)
            self._size = len(s)*2

    def __str__(self): return self.str

    @staticmethod
    def encode4(s: str) -> int:
        "Encodes the RSTP string `s` into an integer"""
        gen = (Dna4.ALPH_D[s[i]]<<(2*(len(s)-i-1)) for i in range(len(s)))
        return reduce(int.__or__, gen, 0)

    @staticmethod
    def decode4 (size:int, n:int)->str:
        """Decodes the given integer `n` into a string of R,S,T,P of `size`"""
        if size % 2 != 0: raise ValueError("Size must be a multiple of 2 to support RSTP:", size)
        return ''.join(Dna4.ALPH[(n>>m)&3] for m in range(size-2, -2, -2))
