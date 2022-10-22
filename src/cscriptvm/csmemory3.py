


from object import CSObject

class ObjectNode(object):

    def __init__(self):
        self.ismarked = False



class ObjectWrapper(ObjectNode):

    def __init__(self, _offset:int, _object:CSObject):
        super().__init__()
        self.__offset = _offset
        self.__object = _object

    def getOffset(self):
        return self.__offset

    def getObject(self):
        return self.__object
    
    def getChildren(self):
        _children = []
        if  not self.__object.isPointer():
            return _children
        
        # array
        return self.__object.getElements()

    def __str__(self) -> str:
        return self.__object.__str__()


class CSMemoryObject(object):

    def __init__(self):
        self.__bucket:list[ObjectWrapper] = []
        self.__nmpntr:dict[int:int] = {}
        self.__freecell:list[int] = []
        self.__allocations:int = 0

        # 
        self.__total_garbage = 0
    
    def makeSlot(self):
        _idx = len(self.__nmpntr)
        self.__nmpntr[_idx] = None
        return _idx
    
    def allocate(self, _csobject:CSObject):
        self.__onallocate()

        if  len(self.__freecell) > 0:
            # reuse free space
            _index = self.__freecell.pop()
            self.__bucket[_index] = ObjectWrapper(_index, _csobject)
            return self.__bucket[_index]

        # append new
        _index = len(self.__bucket)
        self.__bucket.append(ObjectWrapper(_index, _csobject))
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
        _roots:ObjectWrapper = [self.__bucket[idx] for idx in filter(lambda x: x != None, self.__nmpntr.values())]
        while len(_roots) > 0:
            _v = _roots.pop()

            if  not _v.ismarked:
                _v.ismarked = True
                for child in _v.getChildren():
                    _roots.append(child)

    def sweep(self):
        for idx in range(len(self.__bucket)):
            if  self.__bucket[idx] != None:
                if  self.__bucket[idx].ismarked:
                    # reset
                    self.__bucket[idx].ismarked = False
                else:
                    # delete object
                    self.__bucket[idx] = None
                    self.__freecell.append(idx)
                    self.__total_garbage += 1

    def collect(self):
        self.mark ()
        self.sweep()
    
    def collectlast(self):
        self.collect()
        print("GarbageCollected: ", len(self.__freecell))
        print("TotalGarbageCollected: ", self.__total_garbage)
        print("Mem: ", [obj.getObject().__str__() for obj in filter(lambda x:x != None, self.__bucket)])


