#coding=utf-8
from datatype import TypeMeta,datatype
"""
data 'a List = Nil | Cons of 'a * 'a List
class List(metaclass=TypeMeta):
    pass
class Nil(List): pass
class Cons(List):
    def __init__(self,hd,tl):
        self.hd = hd
        self.tl = tl
# old 
"""
@datatype
class List(metaclass=TypeMeta):
    Nil : ( )
    Cons : ("hd","tl")
print ( List )
from m_List import *
print ( List,Nil,Cons )
t = Cons(1,'2')
print( t )
# print ( Nil )
# print ( Cons )
print( List.__annotations__ )
print( Cons.__annotations__ )
print( Nil.__annotations__ )
def sum( lst ):
    if isinstance(lst,Nil) or lst == Nil:
        return 0
    else:
        return lst.hd + sum(lst.tl) 
lst1 = Cons(1,Cons(2,Cons(3,Cons(4,Nil ))))
lst2 = Cons(1,Cons(2,Cons(3,Cons(4,Nil() ))))
print( lst1,sum( lst1 ) )
print( lst2,sum( lst2 ) )

@datatype
class NaturalNum(metaclass=TypeMeta):
    Zero : ()
    Succ : ('num',)
    
from m_NaturalNum import *
zero = Zero()
one = Succ(zero)
print( one,one == Succ(zero),isinstance(one,NaturalNum) )
def plus(a,b):
    if isinstance(a,Zero):
        return b
    else:
        return Succ(plus(a.num,b))
print( plus(one,one) )

print( TypeMeta.__subs__ )
