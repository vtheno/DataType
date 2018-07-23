#coding=utf-8
import sys
from types import ModuleType as module
def datatype(cls):
    """
    usage:
    @datatype
    class List(metaclass=TypeMeta):
        Nil : ( )
        Cons : ("hd","tl")
    # then we get a module ,the module name is 'm_' + class <name>,
    # class List ,then module name is m_List, module has Nil,Cons,List
    """
    mod = module("m_" + cls.__name__,cls.__doc__)
    mod.__dict__.update(cls.__annotations__)
    mod.__dict__.update({cls.__name__:cls})
    sys.modules["m_" + cls.__name__] = mod
    return mod
def makeinit(args):
    template1 = \
    "lambda self,{}:".format(','.join(args))
    template2 = \
    ','.join( ["setattr(self,'{x}',{x})".format(x=i) for i in args] )
    result = template1 + '[' + template2 + ',None][-1]'
    return eval(result)
def makeRepr(args):
    return lambda self : "({} {})".format(self.__name__,','.join([repr(getattr(self,i)) for i in args]))
class TypeMeta(type): 
    __name__ = "TypeMeta"
    __subs__ = {}
    def __new__(cls,name,parents,attrs):
        #print("new metaclass info: ", cls, name, parents, attrs)  
        attrs["__name__"] = name
        #print( attrs.keys() )
        if '__init__' not in attrs.keys() and parents != ( ): 
            attrs["__init__"] = lambda self: None
        if "__repr__" not in attrs.keys():
            attrs["__repr__"] = lambda self: self.__name__
        if parents == ( ):
            if name not in cls.__subs__.keys():
                cls.__subs__[name] = [ ] # init 
        else:
            for p in parents:
                cls.__subs__[p.__name__] += [name]
        tp = type.__new__(cls, name, parents, attrs)
        if "__annotations__" in attrs.keys():
            infos = attrs["__annotations__"]
            #print ("infos:",infos)
            for l_name,args in infos.items():
                #print( l_name,(tp,),{} )
                l_attrs = {}
                if args == ( ):
                    init = lambda self: None
                    Repr = None
                else:
                    init = makeinit(args)
                    Repr = makeRepr(args)
                l_attrs.update( {'__init__':init} )
                if Repr:
                    l_attrs.update( {"__repr__":Repr} )
                infos[l_name] = type(l_name,(tp,),l_attrs)
        return tp
    def __instancecheck__(cls,instance):
        if hasattr(instance,"__name__") and hasattr(cls,"__subs__"):
            name = instance.__name__
            if cls.__name__ in cls.__subs__.keys():
                return name in cls.__subs__[cls.__name__]
        return False
    def __repr__(self):
        return self.__name__
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
            funcs = [list(e.values()) for e in self.tenv[name] ]
            args = [arg for arg in args]
            for typs in funcs:
                flag = 0
                #print( flag, )
                for ty,arg in zip(typs,args):
                    #print( ty,arg )
                    cls = ty.__class__
                    if arg == ty:
                        #print( '==',arg,ty )
                        flag += 1
                    elif (cls == type or cls == TypeMeta) and isinstance(arg,ty):
                        #print( arg.__name__,ty.__name__ )
                        #print( 'isinstance',arg, ty ,cls,funcs.index(typs))
                        flag += 1
                    else:
                        flag = 0
                        break
                if flag:
                    i = funcs.index(typs)
                    #print( self.fenv[name],i,ty,typs )
                    #yield self.fenv[name][i](*args,*kw)
                    return self.fenv[name][i](*args,*kw)
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

class species(object):
    def __init__(self,func):
        self.func = func
    def __get__(self,obj,typ=None):
        def wrapper(*args,**kw):
            return self.func(typ,*args,**kw)
        return wrapper
class static(object):
    def __init__(self,func):
        self.func = func
    def __get__(self,obj,typ=None):
        def wrapper(*args,**kw):
            return self.func(*args,**kw)
        return wrapper
class prop(object):
    def __init__(self,func):
        self.func = func
    def __get__(self,obj,typ=None):
        def wrapper(*args,**kw):
            return self.func(obj,*args,**kw)
        return wrapper()
class class_prop(object):
    def __init__(self,func):
        self.func = func
    def __get__(self,obj,typ=None):
        def wrapper(*args,**kw):
            return self.func(typ,*args,**kw)
        return wrapper()


__all__ = ["TypeMeta","datatype","match",
           "species","static","prop","class_prop"]
