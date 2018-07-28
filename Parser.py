#coding=utf-8
from TVars import *
from Lexical import *
from datatype import TypeMeta,datatype,match,hook
from Sym import *

class ParseError(Exception): pass
@match
def strip( tok : str , toks : [ ] ) -> [str] :
    raise ParseError("strip error ,rest is nil \n tok: {} rest: {}".format(repr(tok),toks))
@match
def strip( tok : str , toks : list) -> [str] :
    x,xs = toks[0],toks[1:]
    if tok == x:
        return xs
    else:
        raise ParseError("strip no match tok ,{} , {}".format(repr(tok),toks))
#print( strip( "a", ["a","b"] ) )
@match
def unpack ( lst : [ ] ) -> (str,[str]):
    raise ParseError("unpack (nil) | {}".format(lst))
@match
def unpack ( lst : list ) -> (str,[str]):
    return lst[0],lst[1:]
"""
E = E binops E ;; binops ['+','-','*','/']
  | Atom
Atom = Num | Sym | Fun
---------------------------------------------
E = T Eopt
Eopt = '+' T Eopt | '-' T Eopt
T = Atom Topt
Topt = '*' Atom Topt | '/' Atom Topt
Atom = Num ...
"""
@match
def atom( t : "if" ,rest : list ) :
    e1,rest1 = parseExpr(rest)
    e2,rest2 = parseExpr( strip("then",rest1) )
    e3,rest3 = parseExpr( strip("else",rest2) )
    return ( (e1,e2,e3) , rest3 )
@match
def atom( t : str , rest : list ):
    return ( ('sym',t),rest )
    #raise ParseError ("ParseAtomError: no match {} , {}".format(repr(t),rest))
def parseAtom( toks : [str] ) -> (object,[str] ):
    t,rest = unpack(toks)
    return atom(t,rest)
def parseExpr( toks : [str] ) -> (object,[str] ):
    exp1,rest1 = parseAtom(toks)
    return parseTerm(exp1,rest1)
def parseTerm( exp1 : object,toks : list ) -> (object,[str] ):
    return (exp1,toks)
def parse(inp : str) -> object :
    return parseExpr( Lex(SpecTab,inp) )
@match
def warpRead( rest : [ ] ,result : object) -> object :
    return result
@match
def warpRead( rest : list ,result : object) -> object:
    out = implode(rest)
    raise ParseError( "readError:\nno parse all ,error in there: \n {} \n index: {}, {}".format(repr(inps),
                                                                                    len(inps) - len(out),
                                                                                                out) )
def read( inps ):
    result,rest = parse(inps)
    return warpRead(rest,result)

print( read("""
if a 
then if b 
     then d 
     else e
else if c
     then f
     else g
""") )
