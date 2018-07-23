#coding=utf-8
class NoMatchError(Exception): pass
class NoSupport(Exception): pass
class match(object):
    def __init__(self,env):
        self.tenv = env
        self.fenv = {} 
    def __warp__(self,name):
        def warp(*args,**kw):
            if kw != {} :
                raise NoSupport("match can not support keyword arguments")
            typs = [list(e.values()) for e in self.tenv[name] ]
            args = [arg for arg in args]
            for typ in typs:
                flag = 0
                for ty,arg in zip(typ,args):
                    cls = ty.__class__
                    if arg == ty:
                        flag += 1
                    elif (cls == type or cls == TypeMeta) and isinstance(arg,ty):
                        #print( arg, ty ,cls,typs.index(typ))
                        flag += 1
                        
                if flag:
                    i = typs.index(typ)
                    #print( self.fenv[name],i )
                    yield self.fenv[name][i](*args,*kw)
            else:
                raise NoMatchError("{} => {} for type(s): {} ".format(name,repr(args),repr(typs)))
        return warp
    def __call__(self,func):
        name = func.__name__
        infos = {}
        infos.update( func.__annotations__ )
        if 'return' in infos.keys():
            infos.pop('return')
        if name not in self.fenv.keys():
            self.fenv[name] = [ ]
        self.fenv[name] += [ func ]
        if name not in self.tenv.keys():
            self.tenv[name] = [ ]
        self.tenv[name] += [ infos ]
        #print( self.tenv )
        return self.__warp__(name)
match = match( {} )                    
from datatype import TypeMeta,datatype

@datatype
class Nat(metaclass=TypeMeta):
    Zero : ()
    Succ : ('num',)
from m_Nat import *
zero = Zero()
one = Succ ( zero )
two = Succ ( one )
@match
def toInt(nat : Zero):
    return 0
@match
def toInt(nat : Succ):
    return 1 + next( toInt(nat.num) )
@match
def toNat( i : 0 ):
    return zero
@match
def toNat( i : int ):
    return Succ ( next(toNat( i - 1 )) )
#print( toInt(zero) )
@match
def plus(a : zero, b : Nat ) -> Nat:
    return b
@match
def plus(a : Succ, b : Nat ) -> Nat :
    return Succ ( a.num ) 

print( next( toInt(one) ) )
print( next( toInt(two) ) )
print( next( toNat(4) ) )
print( next( plus(one,two) ) )
