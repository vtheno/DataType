#coding=utf-8
class Sym(object):
    def __getattr__(self,name):
        return name
Sym = Sym()
__all__ = ["Sym"]
