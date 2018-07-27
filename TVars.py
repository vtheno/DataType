#coding=utf-8
from datatype import TypeMeta,datatype,match,hook
from Sym import Sym
@datatype
class TVar(metaclass=TypeMeta):
    Int : ()
    Str : ()
    Bool : ()
    Any : ()
    Unit : ()
    Tuple : (Sym.tvars,)
    List : (Sym.tvar,)
    Arrow : (Sym.source,Sym.target,)
from m_TVar import *
@hook(Any)
def __eq__(self,other):
    return True
@hook(Tuple)
def __init__(self,*tvars):
    self.tvars = tuple(list(tvars))
@hook(Tuple)
def __eq__(self,other):
    return self.tVars == other
@hook(List)
def __init__(self,tvar):
    self.tvar = [tvar]
@hook(List)
def __eq__(self,other):
    #print( "List:",self.tvar , other)
    return self.tvar == other
@hook(Arrow)
def __eq__(self,other):
    if isinstance(other,Arrow):
        return self.source == other.source and self.target == other.target
    return False
__all__ = ["Int","Str","Bool","Any","Unit","Tuple","List","Arrow",
           "TVar",]

