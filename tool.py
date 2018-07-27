#coding=utf-8
from Sym import *
from datatype import *
from TVars import *
@datatype
class LIST(metaclass=TypeMeta):
    Nil : ()                    # {}
    Cons : (Sym.hd,Sym.tl,)     # {Sym.hd : Any , Sym.tl : LIST}
from m_LIST import *
@hook(Cons)
def __repr__(self):
    return "( {} ... )".format(self.hd)

@match
def toList( lst : list ) -> LIST :
    temp = list(reversed(lst))
    result = Nil
    while temp:
        result = Cons(temp[0],result)
        temp = temp[1:]
    return result
print( toList( list(range(100000)) ) )

