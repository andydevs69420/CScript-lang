
import gc

from object import CSObject


""" CSMemory3

    Uses array|list (single) as linear memory model where ALL objects are stored
"""

class CSMemoryObject(object):

    def __init__(self):
        self.__bucket:list[CSObject] = []
        self.__nmpntr:dict[int:int] = ({})
        self.__freecell:list[int] = []
        self.__allocations:int = 0
        self.__total_garbage = 0
    
    
    def allocate(self, _csobject:CSObject):
        self.__onallocate()

        if  len(self.__freecell) > 0:
            # reuse free space
            _index = self.__freecell.pop()
            if self.__bucket[_index] != None:
                raise Exception("invalid exception")

            _csobject.offset = _index
            self.__bucket[_index] = _csobject
            return self.__bucket[_index]

        # append new
        _index = len(self.__bucket)
        _csobject.offset = _index
        self.__bucket.append(_csobject)
        return self.__bucket[_index]
    
    def __onallocate(self):
        # ======== INCREMENT ALLOC|
        # ========================|
        self.__allocations += 1

        if  self.__allocations >= 500:
            self.collect()
            self.__allocations = 0

    def setAddress(self, _name_pntr:int, _offset:int):
        self.__nmpntr[_name_pntr] = _offset
    
    def getAddress(self, _name_pntr:int):
        return self.__bucket[self.__nmpntr[_name_pntr]]
        
    def mark(self):
        _roots:list[CSObject] = [self.__bucket[idx] for idx in filter(lambda x:x != None, self.__nmpntr.values())]
        while len(_roots) > 0:
            _v = _roots.pop()

            if  not _v.ismarked:
                _v.ismarked = True

                if  _v.isPointer():
                    for child in _v.all():
                        _roots.append(child)

    def sweep(self):
        # below code not working!!
        # this implementation is much better! but does not work!
        for idx in range(len(self.__bucket)):
            if  self.__bucket[idx]:
                if  not self.__bucket[idx].ismarked:
                    self.__total_garbage += 1
                    self.__bucket[idx] = None
                    self.__freecell.append(idx)
                else:
                    self.__bucket[idx].ismarked = False

    def collect(self):
        self.mark ()
        self.sweep()
    
    def collectlast(self):
        self.collect()
        print("Finished -------------" + ("-" * (len(str(self.__total_garbage)) + 1)))
        print("GarbageCollected:     ",  (" " * (len(str(self.__total_garbage)) - len(str(len(self.__freecell))))) + str(len(self.__freecell)))
        print("TotalGarbageCollected:", self.__total_garbage)
        print("MemoryView: ", [obj.__str__() for obj in filter(lambda x:x != None, self.__bucket)])
        # run python gc
        gc.collect()


