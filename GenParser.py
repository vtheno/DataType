#coding=utf-8
from TVars import *
from datatype import datatype,TypeMeta,match,hook
from Lexical import *
from Sym import *
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
from types import GeneratorType as G
def force(g):
    while isinstance(g,G):
        g = next(g)
    return g
class GenParser(object):
    def __init__(self,symtab,inputs):
        self.inp = inputs
        self.symtab = symtab
    def binop(self,sym):
        def inlineBinop(t,tl):
            return Node(sym,[t] + tl)
        return inlineBinop
    def unop(self,sym):
        def inlineUnop(t,tl):
            return MkComb(t,Node(sym,tl))
        return inlineUnop
    def parseAtom(self,m,acc):
        x,self.inp = unpack(self.inp)
        acc1 = MkComb(acc,Atom(x))
        return self.Parser(m,acc1)
    def parseBracket(self,close,m,acc):
        drop,self.inp = unpack(self.inp)
        acc1,inp1 = self.Parser(0,Nil)
        x,self.inp = unpack(inp1)
        if close == x :
            return self.Parser(m,MkComb(acc,acc1))
        else:
            raise Exception("MissingClosingBracket")
    def Terminator(self,obj):
        raise Exception("TerminatorErr")
    def Strip(self,skip):
        def inlineStrip(m,acc):
            acc1,rest = self.Parser(m,acc)
            #print( acc1,skip,rest )
            s1,rest1 = unpack(rest)
            if skip[0] == s1:
                return (acc1,rest1)
            else:
                raise Exception("StripErr")
        return inlineStrip
    def Id(self,m,acc):
        return self.Parser(m,acc)
    def SeqAux(self,funclist,m,n):
        fs = funclist
        acc = [ ]
        while len(fs) > 1:
            f,fs = unpack(fs)
            t,self.inp = f(0,Nil)
            acc += [t]
        f = fs[0] # last f is Id  ,else add supoort Strip 
        t,rest1 = f(m,Nil)  # there m is (Mktree,m,[id | strip sym])
        acc += [t]
        return (acc,rest1)
    def parseSeq(self,funclist,mktree,m,n,acc):
        # mktree = Binop | Unop : make tree 
        # Seq.m is Parser.n ,Seq.n is Parser.m
        # self.funclist is [ ID | Strip "sym"]
        drop,self.inp = unpack(self.inp)
        l,self.inp = self.SeqAux(funclist,m,n)
        return self.Parser(n,mktree(acc,l))
    def Parser(self,m,acc):
        if self.inp == [ ]:
            return (acc,[ ])
        else:
            x,xs = unpack(self.inp)
            n,parsefn = self.symtab(x)
            if m >= n:
                return (acc,self.inp)
            else: # add datatype support in there
                if parsefn == Sym.ParserAtom:
                    return self.parseAtom(m,acc)
                elif isinstance(parsefn,tuple):
                    close = parsefn[0]
                    return self.parseBracket(close,n,acc)
                elif isinstance(parsefn,list):
                    head,n,funclist = parsefn # parsefn len is 3 
                    funclist = [ self.Strip(func) if isinstance(func,list) else self.Id \
                                 for func in funclist ]
                    if head[0] == "binop":
                        mktree = self.binop(head[1])
                    elif head[0] == "unop":
                        mktree = self.unop(head[1])
                    else:
                        raise Exception("MkTreeErr")
                    return self.parseSeq(funclist,mktree,n,m,acc) # Seq.m = n Seq.n = m
                elif parsefn == Sym.Terminator:
                    return self.Terminator(m)
                else:
                    raise Exception("ParserErr")
                
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
                                      Sym.id,
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
in a - a * a + a - 1""")
src = """
func if (a)
     then if let c = 233 in c 
          then d 
          else f
     else let h = g 
          in h
"""
#lst = Lex(SpecTab,src)
#print ( lst )
g = GenParser(SymTab,lst)
out =g.Parser(0,Nil)
print( force(out) )
"""
Parse = Atom 
      | Bracket
      | Seq
      | Terminator
"""
