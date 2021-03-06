#coding=utf-8
from TVars import *
from datatype import match
def Mem( x : str , lst : [ (str,[str] ) ] ) -> bool :
    temp = lst
    while temp:
        t,temp = temp[0],temp[1:]
        if t == x:
            return True
    return False
def Get(x : str, lst : [ (str,[str]) ] ) -> [str] :
    result = [ ]
    temp = lst
    while temp:
        (t,c),temp = temp[0],temp[1:]
        if x == t:
            return c
    return result
def IsDigit( x : str ) -> bool :
    return '0' <= x <= '9'
def IsDigit( x :str ) -> bool:
    return "0" <= x <= "9"
def IsLetter( x : str ) -> bool:
    return "a" <= x <= "z" or "A" <= x <= "Z"
def IsLetterOrDigit( x : str ) -> bool:
    return ("a" <= x <= "z" or "A" <= x <= "Z") or "0" <= x <= "9"
def IsSeparator( x : str ) -> bool:
    # \\n \\t
    return x == " " or x == "\n" or x == "\t" 
explode = list
def implode( lst : List(str) ) -> str:
    return ''.join(lst)
def GetSymbol ( spectab , tok, lst ):
    temp = lst
    while temp:
        x,temp = temp[0],temp[1:]
        l = [x] + temp
        if Mem(x,Get(tok,spectab)):
            tok += x
        else:
            return (tok,l)
    return (tok,[ ])
def GetTail(p , buf ,lst ):
    #print( "GetTail",p,buf,lst)
    result = buf
    temp = lst
    while temp :
        x,temp = temp[0],temp[1:]
        if p(x):
            result = [x] + result
            continue
        else:
            temp = [x] + temp # fix a miss tok
            return ( ''.join(list(reversed(result))),temp )
    return ( ''.join(list(reversed(result))),temp )
class GetNextTokenErr(Exception) : pass
def GetNextToken(spectab : list ,lst : [ ]):
    if lst == [ ]:
        raise GetNextTokenErr("{} length < 1 !".format(temp))
    elif lst == [Any]:
        return (lst[0],[])
    else:
        temp = lst
        x,l = temp[0],temp[1:]
        c,cs = l[0],l[1:]
        if IsLetter(x):
            return GetTail (IsLetterOrDigit,[x],l)
        elif IsDigit(x):
            return GetTail (IsDigit,[x],l)
        else:
            if Mem(c,Get(x,spectab)):
                return GetSymbol( spectab,implode([x,c]),cs)
            return (x,l)
def Tokenise( spectab : List(Tuple(str,List(str))) , lst : List(str) ) -> List(str) :
    temp = lst
    result = [ ]
    while temp:
        x,l1 = temp[0],temp[1:]
        l = [x] + l1
        #print( "now =>",x,temp)
        if IsSeparator(x):
            #print( "IsSeparator(x)",repr(x),temp )
            temp = l1
        else:
            t,l2 = GetNextToken(spectab,l)
            temp = l2
            result = result + [ t ]
    return result

SpecTab = [ ("=",["<",">","="]),
            (">",["<",">"]),
            ("<",["<",">"]),
            ("==",[">"])]
def Lex(spectab,inp):
    """ spectab example:
    SpecTab = [ ("=",["<",">","="]),
                (">",["<",">"]),
                ("<",["<",">"]),
                ("==",[">"]) ]
    => =< == , >< >> ,<< <> ,==>
    """
    inps = explode(inp)
    return Tokenise(spectab,inps )
__all__ = ["Lex","Tokenise",
           "GetNextToken","GetTail","GetSymbol",
           "IsSeparator","IsDigit","IsLetter","IsLetterOrDigit",
           "explode","implode",
           "Mem","Get","SpecTab","GetNextTokenErr"]

