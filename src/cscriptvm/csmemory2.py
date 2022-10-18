


class ObjectWrapper(object):
    """ ObjectWrapper class
    """

    def __init__(self, _offset:int, _csobject:object):
        self.__object:object = _csobject
        self.__rcount:int    = 0
        self.__offset:int    = _offset
    
    def increment(self):
        self.__rcount += 1
    
    def decrement(self):
        self.__rcount -= 1
    
    def getObject(self):
        return self.__object
    
    def getOffset(self):
        return self.__offset
    
    def __str__(self):
        return self.__object.toString().__str__()
    


class CSMemory:

    MEMORY:list[ObjectWrapper] = []

    @staticmethod
    def CSMalloc(_csobject:object) -> ObjectWrapper:
        _offset = len(CSMemory.MEMORY)
        CSMemory.MEMORY.append(ObjectWrapper(_offset, _csobject))
        return CSMemory.MEMORY[-1]
    
    @staticmethod
    def getObjectAt(_index:int):
        return CSMemory.MEMORY[_index]

    @staticmethod
    def incrementAt(_index:int):
        if  _index != None:
            CSMemory.MEMORY[_index].increment()

    @staticmethod
    def decrementAt(_index:int):
        if  _index != None:
            CSMemory.MEMORY[_index].decrement()