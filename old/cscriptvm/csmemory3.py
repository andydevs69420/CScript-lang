
import gc

from object import CSObject


""" CSMemory3

    Uses array|list (single) as linear memory model where ALL objects are stored
"""


class CSMemoryObject(object):

    def __init__(self):
        self.__bucket:list[CSObject] = ([
            # +------------+
            # | CSObject 0 |
            # +------------+
            # | CSObject . |
            # +------------+
            # | CSObject N |
            # +------------+
        ])

        self.__nmpntr:dict[int:int] = ({
            # var_x: 0,
            # var_y: 1,
            # var_N: 1000...
        })

        self.__freecell:list[int] = ([
            # +-----------------------+
            # | self.__bucket index N |
            # +-----------------------+
            # | self.__bucket index ? |
            # +-----------------------+
        ])

        self.__allocations:int = 0
        self.__total_garbage = 0
    
    def allocate(self, _csobject:CSObject):
        self.__onallocate()

        if  _csobject.offset != -69420:
            raise Exception(f"{_csobject.__str__()} is already in memory at index {_csobject.offset}!!!")

        if  len(self.__freecell) > 0:
            # reuse free space
            _index = self.__freecell.pop()
            if self.__bucket[_index] != None:
                raise Exception("invalid allocation|collision of objects")

            _csobject.offset = _index
            self.__bucket[_index] = _csobject
            return self.__bucket[_index]

        # append new
        _index = len(self.__bucket)
        _csobject.offset = _index
        self.__bucket.append(_csobject)
        return self.__bucket[_index]
    
    def __onallocate(self):
        from .csvm import CSVM as VM
        if  not VM.isrunning():
            del VM
            return
        # ======== INCREMENT ALLOC|
        # ========================|
        self.__allocations += 1

        # run collector every 500 or more alloc
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

            if  not _v.marked:
                _v.marked = True

                for child in _v.all():
                    _roots.append(child)

    def sweep(self):
        for idx in range(len(self.__bucket)):
            if  self.__bucket[idx]:
                if  not self.__bucket[idx].marked:
                    self.__total_garbage += 1
                    self.__bucket[idx] = None
                    self.__freecell.append(idx)
                else:
                    self.__bucket[idx].marked = False

    def collect(self):
        self.mark ()
        self.sweep()
    
    def collectlast(self):
        self.collect()

        _trailing = ("-" * (len(str(self.__total_garbage)) + 2))

        print("+-Finished--------------" + _trailing + "+")
        print("| GarbageCollected:     ",  (" " * (len(str(self.__total_garbage)) - len(str(len(self.__freecell))))) + str(len(self.__freecell)) + " |")
        print("+-----------------------" + _trailing + "+")
        print("| TotalGarbageCollected:", str(self.__total_garbage) + " |")
        print("+-----------------------" + _trailing + "+")
        print("MemoryView: ", [obj.__str__() for obj in filter(lambda x:x != None, self.__bucket)])
        self.__bucket.clear()
        # run python gc
        gc.collect()


def __toString__(_map):
    _keys = _map.keys()

    _attr = ""

    _index = 0
    for _k in _keys:
        _value = _map.get(_k)

        _string= ""
        if  _value is _map:
            _string = "{self}"
        else:
            _string = _value.__str__()
        
        _attr += f"{_k}: {_string}"

        if  _index < len(_keys) - 1:
            _attr += ", "
        
        _index += 1

    return "{" + _attr + "}"