#coding=utf-8
from optimze import Code
import dis
from types import FunctionType
from collections import OrderedDict
from opcode import opmap,opname
def prettyCode(co):
    print( " argcount:" , co.co_argcount)
    print( " kwonlyargcount:" , co.co_kwonlyargcount)
    print( " nlocals:" , co.co_nlocals)
    print( " stacksize:" , co.co_stacksize)
    print( " flags:" , co.co_flags)
    print( " codestring:" , list(co.co_code))
    print( " consts:" , co.co_consts)
    print( " names:" , co.co_name)
    print( " varnames:" , co.co_varnames)
    print( " filename:" , co.co_filename)
    print( " name:" , co.co_name)
    print( " firstlineno:" , co.co_firstlineno)
    print( " lnotab:" , co.co_lnotab)
    print( " freevars:" , co.co_freevars)
    print( " cellvars:" , co.co_cellvars)
class Transfor(object):
    def __init__(self,**kw):
        self.local_env = OrderedDict(kw)
        vals = kw.keys()
        self.env_local = dict( zip(vals,range(len(vals))) ) 
class CONST(Transfor): 
    # LOAD_GLOBAL convert to LOAD_CONSTS
    pass
class FAST(Transfor):
    def process(self):
        code = [i for i in self.code.co_code]
        varnames = list(self.code.co_varnames)
        offset = len(varnames)
        new_varnames = varnames + list(self.env_local.keys())
        names = self.code.co_names
        results = dict([(i,n) for n,i in zip(names,range(len(names))) if n in self.local_env.keys()])
        argcount = self.code.co_argcount
        #new_names = [n for n in names if n not in self.local_env ]
        #print( results )
        n = 0
        while n < len(code):
            op,arg = code[n],code[n+1]
            #print( opname[op],arg ,op == arg in results.keys() )
            if op == opmap["LOAD_GLOBAL"] and arg in results.keys():
                code[n] = opmap["LOAD_FAST"]
                #print( offset,self.env_local[results[arg]] )
                code[n+1] = offset + self.env_local[results[arg]] 
            n+= 2
        new = Code(argnames = new_varnames[0:argcount],
                   local_vars = new_varnames[argcount:],
                   consts = self.code.co_consts,
                   names = self.code.co_names,
                   codestring = code,
                   stacksize = self.code.co_stacksize,
                   flags = self.code.co_flags,
                   name = self.code.co_name)
        new.kwonlyargcount = self.code.co_kwonlyargcount
        new.firstlineno = self.code.co_firstlineno
        new.filename = self.code.co_filename
        new.lnotab = self.code.co_lnotab
        new.cellvars = self.code.co_cellvars
        new.freevars = self.code.co_freevars
        new.argcount = argcount + len(self.local_env.keys())
        newCo = new.build()
        self.code = newCo
    def __call__(self,func):
        self.code = func.__code__
        self.global_env = func.__globals__
        _argdef = func.__defaults__
        if _argdef is None:
            _argdef = [ ]
        _argdef += list(self.local_env.values())
        self.process()
        _name = func.__name__
        _closure = func.__closure__
        if _closure is None:
            _closure = ( )
        new_func = FunctionType(self.code,
                                self.global_env,
                                _name,
                                tuple(_argdef),
                                _closure)
        #prettyCode(self.code)
        return new_func
#help(FunctionType)
@FAST(a=1)
def func(b):
    return a + b
print( func(1) )
dis.show_code(func)

@FAST(lst=list(range(995)),acc=0)
def Sum():
    if lst == [ ]:
        return acc
    return Sum(lst=lst[1:],acc=acc + lst[0])


from types import GeneratorType
def force(g):
    while isinstance(g,GeneratorType):
        g = next(g)
    return g
import time
t1 = time.clock()
print( Sum() )
tc = time.clock()
print( sum(list(range(995) ) ) )
te = time.clock()
print( (tc - t1) * 1000 , (te - tc)*1000 )

