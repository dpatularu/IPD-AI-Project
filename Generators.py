"""Contains factory classes for generating sequences such as
randomized Cs or Ds, or all Ts, for example"""

from asyncio import streams
import random



class CD_Generator:
    """Contains a bunch of static functions for generating either
    strategies or initial states, anything consisting of 'C's or 'D's"""

    @staticmethod
    def random (k:int)->str:
        """Random string of length `k` of Cooperate or Defect, (C or D)"""
        return "".join(random.choices(("C", "D"), k=k))
    
    @staticmethod
    def all_cooperate (k:int)->str:
        """String of length `k` of all `C`s"""
        return "C" * k
    
    @staticmethod
    def all_defect (k:int)->str:
        """String of length `k` of all `D`s"""
        return "D" * k
    
    @staticmethod
    def from_number (k:int, n:int)->str:
        """String of length `k` decoded from the number `n`"""
        result = bytearray("C"*k, "ASCII")
        step :int = 1
        for i in range(k-1,-1,-1):
            if n & step:
                result[i]+=1
            step <<= 1
        return str(result, "ASCII")



class RTSP_Generator:
    """Contains a bunch of static functions for generating Initial States
        consisting of 'R', 'T', 'S', or 'P'"""

    @staticmethod
    def random (k:int)->str:
        """String of length `k` of random letters from `R`,`T`,`S`,`P`"""
        return "".join(random.choices(("R", "T", "S", "P"), k=k))
    
    @staticmethod
    def all_sucker (k:int)->str:
        """String of length `k` of all `S`"""
        return "S" * k
    
    @staticmethod
    def all_tempted (k:int)->str:
        """String of length `k` of all `T`"""
        return "T" * k
    
    @staticmethod
    def all_reward (k:int)->str:
        """String of length `k` of all `R`"""
        return "R" * k
    
    @staticmethod
    def all_penalty (k:int)->str:
        """String of length `k` of all `P`"""
        return "P" * k
