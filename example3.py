from datatype import TypeMeta,datatype,match
@datatype
class Nat(metaclass=TypeMeta):
    Zero : ()
    Succ : ('num',)
from m_Nat import *
@match
def toInt(nat : Zero) -> int :
    return 0
@match
def toInt(nat : Succ) -> int :
    return 1 + toInt( nat.num ) 
    
zero = Zero ()
one = Succ ( zero )
two = Succ ( one )    
@match
def plus(a : Zero, b : Nat) -> Nat :
    return b
@match
def plus(a : Succ, b : Nat ) -> Nat:
    return plus(a.num,Succ( b ) )
print( toInt ( plus ( one,two ) ) )
# output => 3

@match
def toNat( i : 0) -> Nat:
    return zero
@match
def toNat( i : int ) -> Nat :
    return Succ ( toNat( i - 1 ) )
    
print( toNat (99) )
                
# match 
