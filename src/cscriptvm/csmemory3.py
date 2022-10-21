


from object import CSObject

class ObjectNode(object):

    def __init__(self):
        self.ismarked = False
        self.children:list = []


class ObjectWrapper(ObjectNode):

    def __init__(self, _object:CSObject):
        super().__init()
        self.object = _object


class CSMemoryObject(object):

    def __ini__(self):
        self.__bucket:list[ObjectWrapper] = []
        self.__nmpntr:dict[int:int] = {}

        self.freecell:int = []
    
    def allocate(self, _csobject:CSObject):
        if  len(self.freecell) > 0:
            self.__bucket[self.freecell.pop()] = ObjectWrapper(_csobject)
            return self.__bucket[self.freecell.pop()]

        # append new
        self.__bucket.append(ObjectWrapper(_csobject))
        return self.__bucket[-1]
        
    def mark(self):
        _roots:ObjectWrapper = [self.__bucket[idx] for idx in filter(lambda x: x != None, self.__nmpntr.values())]
        while len(_roots) > 0:
            _v = _roots.pop()

            if  not _v.ismarked:
                _v.ismarked = True
                for child in _v.children:
                    _roots.append(child)

    def sweep(self):
        for idx in range(len(self.__bucket)):
            if  self.__bucket[idx].ismarked:
                # reset
                self.__bucket[idx].ismarked = False
            else:
                # delete object
                self.__bucket[idx] = None
                self.freecell.append(idx)

    def collect(self):
        self.mark ()
        self.sweep()


