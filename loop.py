#coding=utf-8
from TVars import *
from datatype import datatype,TypeMeta,match,hook
from Lexical import *
from Sym import *
class Stack(object):
    def __init__(self,size=256):
        self.s = [None] * size
        self.top = 0
    def __repr__(self):
        return "{} : ".format(self.top) + repr(self.s[0:10]) 
    @property
    def IsEmpty(self):
        return self.top == 0
    def push(self,val):
        self.s[self.top] = val
        self.top += 1
        return self.top
    def pop(self):
        self.top -= 1
        val = self.s[self.top]
        self.s[self.top] = None
        return val
@datatype
class Tree(metaclass=TypeMeta):
    Nil : ()
    Atom : (Sym.s,)
    Comb : (Sym.t1,Sym.t2,)
    Node : (Sym.s,Sym.ts,)
from m_Tree import *
nil = Nil
def exception(name):
    globals()[name] = type(name,(Exception,),{})
    return globals()[name]
exception(Sym.NilRightArg) # exception NilRightArg
def MkComb( t1 ,t2 ):
    if t1 == Nil:
        return t2
    elif t2 == Nil:
        raise NilRightArg
    else:
        return Comb(t1,t2)
exception(Sym.UnPackErr)
def unpack(inp:list):
    if inp == []:
        raise UnPackErr
    return inp[0],inp[1:]

def getIndex( lst , val ):
    if lst == [ ]:
        raise Exception
    else:
        if lst[0] == val:
            return 0
        else:
            return 1 + getIndex(lst[1:],val)

def getIndex_loop(lst,val):
    if lst == [ ]:
        raise Exception
    s = Stack ( len(lst) )
    s.push( lst )
    index = 0
    while not s.IsEmpty:
        #print( s )
        head = s.pop () 
        #print( head[0] )
        if head[0] == val:
            break
        else:
            head = head[1:]
            s.push(head)
            index+=1
    #print( s )
    #print( index )
    return index
# print (getIndex_loop (list(range(999999) ) , 10000 ) )
# print( list (range (999999)).index(10000) ) 
class GenParser(object):
    def __init__(self,symtab,inputs):
        self.inp = inputs
        self.symtab = symtab
        self.s = Stack ( len(self.inp)  *  10)
    def binop(self,sym):
        def inlineBinop(t,tl):
            return Node(sym,[t] + tl)
        return inlineBinop
    def unop(self,sym):
        def inlineUnop(t,tl):
            return MkComb(t,Node(sym,tl))
        return inlineUnop
    def Strip(self,skip):
        def inlineStrip(m,acc):
            acc1,rest = self.Parser_loop(m,acc)
            s1,rest1 = unpack(rest)
            if skip[0] == s1:
                return (acc1,rest1)
            else:
                raise Exception("StripErr")
        return inlineStrip
    def Id(self,m,acc):
        return self.Parser_loop(m,acc)
    def parseAtom(self,m,acc):
        x,self.inp = unpack(self.inp)
        acc1 = MkComb(acc,Atom(x))
        return self.Parser(m,acc1)
    def Terminator(self,obj):
        raise Exception("TerminatorErr")
    def parseBracket(self,close,m,acc):
        drop,self.inp = unpack(self.inp)
        acc1,inp1 = self.Parser(0,Nil)
        x,self.inp = unpack(inp1)
        if close == x :
            return self.Parser(m,MkComb(acc,acc1))
        else:
            raise Exception("MissingClosingBracket")
    def Parser_loop (self,m,acc):
        self.s.push( acc )
        while not self.s.IsEmpty :
            print( self.s )
            print( "inp:",self.inp )
            print( "acc:",acc)
            acc = self.s.pop ()
            if self.inp == [ ]:
                break
            else:
                x,xs = unpack(self.inp)
                n,parsefn = self.symtab(x)
                if m >= n :
                    #self.s.push( acc )##,self.inp) )
                    break
                else:
                    if parsefn == Sym.ParserAtom:
                        x,self.inp = unpack(self.inp)
                        acc = MkComb(acc,Atom(x))
                        self.s.push( acc )#,self.inp) )
                        continue
                    elif parsefn == Sym.Terminator:
                        raise Exception ("TerminatorErr")
                    elif isinstance(parsefn,tuple):
                        close = parsefn[0]
                        drop,self.inp = unpack(self.inp)
                        acc1,inp1 = self.Parser_loop(0,Nil) # how fix it
                        x,self.inp = unpack(inp1)
                        if close == x :
                            acc = MkComb(acc,acc1)
                            self.s.push( acc )#(acc,self.inp) )
                            continue
                        else:
                            raise Exception("MissingClosingBracket")
                    elif isinstance(parsefn,list):
                        head,n,funclist = parsefn # parsefn len is 3 
                        fs = [ self.Strip(func) if isinstance(func,list) else self.Id \
                                     for func in funclist ]
                        if head[0] == "binop":
                            mktree = self.binop(head[1])
                        elif head[0] == "unop":
                            mktree = self.unop(head[1])
                        else:
                            raise Exception("MkTreeErr") # seq_m = n ,seq_n = m
                        seq_m,seq_n = n , m
                        drop,self.inp = unpack(self.inp)
                        seq_acc = [ ]
                        while len(fs) > 1:
                            f,fs = unpack(fs)
                            t,self.inp = f(0,Nil)
                            seq_acc += [t]
                        f = fs[0]           # last f is Id  ,else add supoort Strip 
                        t,self.inp = f(seq_m,Nil)  # there m is (Mktree,m,[id | strip sym])
                        seq_acc += [t]
                        m = seq_n
                        acc = mktree(acc,seq_acc)
                        self.s.push( acc )
                        continue
                    else:
                        raise Exception ("ParserErr")
        return acc,self.inp


def SymTab(x):
    #print( "symtab:",x )
    if x == ".":
        return (0,Sym.Terminator)
    elif x == "(":
        return (10,(")",)) # bracket
    elif x == ")":
        return (0,Sym.Terminator)
    elif x == "+":
        return (6,[("binop","ADD"),5,[Sym.id]])
    elif x == "-":
        return (6,[("binop","SUB"),5,[Sym.id]])
    elif x == "*":
        return (7,[("binop","MUL"),8,[Sym.id]])
    elif x == "if":
        return (10,[("unop","Cond"),0,[["then"],
                                       ["else"],
                                       Sym.id]])
    elif x == "let":
        return (10,[("unop","LET"),0,[["="],
                                      ["in"],
                                      ["end"],
                                  ]] )
    elif x == "end":
        return (0,Sym.Terminator)
    elif x == "=":
        return (0,Sym.Terminator)
    elif x == "in":
        return (0,Sym.Terminator)
    elif x == "then":
        return (0,Sym.Terminator)
    elif x == "else":
        return (0,Sym.Terminator)
    else:
        return (10,Sym.ParserAtom)
lst = Lex(SpecTab,"""
let a = 233 
in a - a * a + 2 end""")
g = GenParser(SymTab,lst)
r = g.Parser_loop(0,Nil) 
print ( r )
