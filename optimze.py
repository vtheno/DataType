#coding=utf-8
from types import FunctionType,CodeType,GeneratorType
from opcode import opmap,opname
import dis
class Code(object):
    def __init__(self,
                 argnames : [str] ,local_vars : [str] ,
                 consts : [object] ,names : [str],
                 codestring : [int] ,
                 stacksize : int,flags : int,
                 name : str):
        self.varnames = argnames + local_vars
        self.consts = consts
        self.names = names

        self.argcount = len(argnames)
        self.kwonlyargcount = 0
        self.nlocals = len(self.varnames)

        self.codestring = codestring

        self.stacksize = stacksize
        self.flags = flags

        self.firstlineno = -1
        self.lnotab = b''

        self.name = name
        self.filename = "<" + name + ">"

        self.freevars = tuple ()
        self.cellvars = tuple ()
    def build(self):
        # print( " argcount:" , self.argcount)
        # print( " kwonlyargcount:" , self.kwonlyargcount)
        # print( " nlocals:" , self.nlocals)
        # print( " stacksize:" , self.stacksize)
        # print( " flags:" , self.flags)
        # print( " codestring:" , self.codestring)
        # print( " consts:" , self.consts)
        # print( " names:" , self.name)
        # print( " varnames:" , self.varnames)
        # print( " filename:" , self.filename)
        # print( " name:" , self.name)
        # print( " firstlineno:" , self.firstlineno)
        # print( " lnotab:" , self.lnotab)
        # print( " freevars:" , self.freevars)
        # print( " cellvars:" , self.cellvars)
        code = CodeType(self.argcount,       # argcount
                        self.kwonlyargcount, # kwonlyargcount
                        self.nlocals,        # nlocals
                        self.stacksize,      # stacksize
                        self.flags,          # flags
                        bytes(self.codestring), # codestring
                        tuple(self.consts),     # consts
                        tuple(self.names),      # names
                        tuple(self.varnames),   # varnames
                        self.filename,          # filename
                        self.name,              # name
                        self.firstlineno,       # firstlineno
                        self.lnotab,            # lnotab
                        self.freevars,          # freevars
                        self.cellvars,          # cellvars
                    )
        return code
label_env = {}
def process_label(pc,args): # can async in here
    global label_env
    yield label_env[args]
def Inst(op_name,args):
    pc = yield
    #print( pc )
    #yield 
    print( pc,op_name,args )
    if op_name == "LABEL":
        global label_env
        label_env[args] = pc
        yield opmap["NOP"],0
    else:
        if isinstance(args,str):
            args = process_label(pc,args)
        yield opmap[op_name],args
def For(*Instructions):
    result = [ ]
    pc = 0
    # Instructions = list(Instructions)
    # print( len(Instructions) )
    for obj in Instructions:
        none = next(obj)   
        # next(obj) then pc = yield , yield None is current next(obj) return val
        # val = obj.send(pc)
        # because of pc = yield ,now we send(pc),then obj local pc assgin of For pc
        # and obj.send(pc) will return next yield <val> , val is <val>
        result.extend( obj.send(pc)  )
        pc += 2
    #print( result )
    return [next(r) if isinstance(r,GeneratorType) else r for r in result]
def pretty(codes):
    n = 0
    print ("-----pretty-----")
    while n < len(codes):
        print( n,opname[codes[n]],codes[n+1] )
        n+=2
    print ("-----pretty-----")
"""
byte = For( Inst("LOAD_FAST",0),
            Inst("LOAD_FAST",1),
            Inst("BINARY_ADD",0),
            Inst("POP_JUMP_IF_FALSE","label1"),
            Inst("PRINT_EXPR",0),
            Inst("LABEL","label1"),
            Inst("RETURN_VALUE",0))
# 模拟 loop recursion jump goto 
# print (byte)

pretty( byte )

c = Code( argnames = [ ] ,
          local_vars = ['a','b'] , 
          consts = [ ], 
          names = [ ],
          codestring = byte,
          stacksize = 2,
          flags = 64,
          name = 'c').build()
dis.dis(c)
"""
__all__ = ["Code"]
