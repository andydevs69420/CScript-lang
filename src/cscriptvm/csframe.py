
from .csmemory3 import CSMemoryObject

from astnode.utils.compilable import Instruction

from base.csobject import CSObject
class Frame(object):

    def __init__(self, _instructions:list[Instruction]):
        self.localmem:list[CSObject] = []
        self.returned = False
        self.ipointer = 0

        # ======== LIST OF INTRUCTIONS|
        # ============================|
        self.instructions:list[Instruction] = _instructions

    def store_local(self, _index:int, _csobject:CSObject):
        if  len(self.localmem) <= 0 or _index >= len(self.localmem):
            self.localmem.append(_csobject)
            return
        # set
        self.localmem[_index] = _csobject
    
    def getLocalAt(self, _index:int):
        return self.localmem[_index]

    def setPointer(self, _index:int):
        self.ipointer = _index

    def next(self):
        _code = self.instructions[self.ipointer]
        self.ipointer += 1
        return _code
    
    def setReturn(self, _returned:bool):
        self.returned = _returned

    def isReturned(self):
        return self.returned or self.ipointer >= len(self.instructions)
    
    def cleanup(self):
        self.localmem.clear()
        del self


