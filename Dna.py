"""Contains the Dna and Dna4 classes"""


from functools import reduce
from Node import CD, RSTP


class Dna:
    """Stores a string of Cs and Ds, otherwise known as a bunch of bits.
    
    Is stored internally as a number and size. But...
    - The constructor can accept a string rep of the Dna
    - You can use one of the Dna Generators in `Generators`

    You can see `Node.CD` for what each bit represents.

    The bits read right-to-left VALUE WISE, so "CDCC" = int:4, but index:1 = D
    """

    __slots__ = ['_val', '_size']
    def __init__(self, x: any, size: int = 0): #TODO: Dispatch init?
        """Create a Dna objec with the given value and optional size.

        Paramaters
        ----------
        (x: `str`) :
            Takes a string of letters to parse into a value and size.
            For example, "CDCC" would given a Dna object of value 4 and size 4.
        (x: `Dna`) :
            Makes a copy.
        (x: `int`, size: `int`) :
            Creates a Dna object of `size` and bits set to the value of integer `x`.
        """
        if isinstance(x, str):
            self.str = x
        elif isinstance(x, Dna):
            self._val :int = x.val
            self._size :int = x.size
        elif isinstance(x, int):
            self._val: int = x
            self._size: int = max(size, x.bit_length(), 1)
        else: raise TypeError(x)
        self.size = self._size # Verify using setter
        self.val = self._val   # Verify using setter

    # # # # # # # # # #
    #   PROPERTIES    #
    # # # # # # # # # #

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
        return self.decode(self.size, self.val)

    @str.setter
    def str(self, s: str):
        if s[0]=="C" or s[0]=="D":
            self._val = self.encode(s)
            self._size = len(s) * CD.size()
        else:
            self._val = self.encode4(s)
            self._size = len(s) * RSTP.size()

    # # # # # # # # # #
    #    IMPLICITS    #
    # # # # # # # # # #

    def __str__(self) -> str:
        return self.str

    def __int__(self) -> int:
        return self.val

    __index__ = __int__

    def __len__(self) -> int:
        return self.size

    def index(self, i:int)->int:
        "Gets the `i`th bit and further in this Dna. BitAnd for which bits you want to keep. Slices not supported."
        while i<0: i += self.size
        if i >= self.size: raise IndexError("Index too big:",i,">=",self.size)
        return self.val >> (self.size - i - 1)

    def getCD (self, i:int)->CD:
        "Gets the `i`th CD action in this Dna. Slices not supported."
        return CD(self.index(i) & 1)

    def getRSTP (self, i:int)->RSTP:
        "Gets the `i`th RSTP action in this Dna. Slices not supported."
        return RSTP(self.index(i*2+1) & 3)

    __getitem__ = getCD

    def __hash__(self) -> int:
        return hash(str(self))

    # # # # # # # # # #
    #   OPERATIONS    #
    # # # # # # # # # #

    def __eq__(self, o) -> bool:
        if isinstance(o, (CD, RSTP)):
            o = str(o)
        elif isinstance(o, int):
            o = Dna(o, self.size)
        if not isinstance(o, Dna):
            o = Dna(o)
        return self.val == o.val and self.size == o.size

    def __bop__(self, op, t) -> bool:
        "Helper function for calling binary operations"
        if isinstance(t, (CD, RSTP)):
            t = str(t)
        if not isinstance(t, Dna):
            t = Dna(t)
        return op(self.val, t.val)

    def __lt__(self, t): return self.__bop__(int.__lt__, t)
    def __le__(self, t): return self.__bop__(int.__le__, t)
    def __gt__(self, t): return self.__bop__(int.__gt__, t)
    def __ge__(self, t): return self.__bop__(int.__ge__, t)

    def __op__(self, op, t) -> object:
        "Performs the given integer operation like | & ^, with LHS=self, returning a new Dna"
        if not isinstance(t, Dna):
            t = Dna(t)
        return self.__class__(Dna(op(self.val, t.val), max(self.size, t.size)))

    def __or__  (self, t): return self.__op__(int.__or__,   t)
    def __ror__ (self, t): return self.__op__(int.__ror__,  t)
    def __and__ (self, t): return self.__op__(int.__and__,  t)
    def __rand__(self, t): return self.__op__(int.__rand__, t)
    def __xor__ (self, t): return self.__op__(int.__xor__,  t)
    def __rxor__(self, t): return self.__op__(int.__rxor__, t)

    def __lshift__(self, t):
        if isinstance(t, (CD, RSTP)):
            t = str(t)
        if not isinstance(t, Dna):
            t = Dna(t)
        return self.__class__(Dna(self.val << t.size | t.val, self.size+t.size))

    def __rshift__(self, t):
        if isinstance(t, (CD, RSTP)):
            t = str(t)
        if not isinstance(t, Dna):
            t = Dna(t)
        return self.__class__(Dna(self.val >> t.size | t.val << (self.size - t.size), self.size))

    def __invert__(self):
        return self.__class__(Dna(self.val ^ self.maxValue, self.size))

    # # # # # # # # # #
    #   ALGORITHMS    #
    # # # # # # # # # #

    @staticmethod
    def encode(s: str) -> int:
        """Encodes the CD string `s` into an integer"""
        step: int = 2**(len(s)-1)
        iter = [(step >> i) for i in range(len(s)) if CD[s[i]]]
        return reduce(int.__or__, iter, 0)

    @staticmethod
    def decode(size: int, n: int) -> str:
        """Decodes the given integer `n` into a string of Cs and Ds of `size`"""
        return ''.join([str(CD(n >> (size-1-m) & 1)) for m in range(size)])

    @staticmethod
    def encode4(s: str) -> int:
        "Encodes the RSTP string `s` into an integer"""
        iter = [RSTP[s[i]]<<(2*(len(s)-i-1)) for i in range(len(s))]
        return reduce(int.__or__, iter, 0)

    @staticmethod
    def decode4(size:int, n:int)->str:
        """Decodes the given integer `n` into a string of R,S,T,P of `size`"""
        if size % 2 != 0: raise ValueError("Size must be a multiple of 2 to support RSTP:", size)
        return ''.join([str(RSTP((n>>m)&3)) for m in range(size-2, -2, -2)])

    def countDefects(self)->int:
        "Returns the number of Defect actions int this Dna"
        return self.val.bit_count()

    def countCoops(self)->int:
        "Returns the number of Cooperate actions in this Dna"
        return self.size - self.countDefects()

#================================================================================================================================

class Dna4 (Dna):
    """Subclass of Dna, uses RSTP instead of CD"""

    def __init__(self, x: int | str, size: int = 0):
        """Creates a piece of DNA. You can either pass in an integer
        and a size or a string of R,S,T, or P"""
        super().__init__(x, size*RSTP.size())
    
    @Dna.str.getter
    def str(self)->str:
        return self.decode4(self.size, self.val)

    __getitem__ = Dna.getRSTP # Change default from getCD
