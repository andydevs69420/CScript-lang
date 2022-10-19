
# ======= object|
# ==============|
from object.csobject import CSObject
# ==============|




class ObjectWrapper(object):
    """ ObjectWrapper class
    """

    def __init__(self, _offset:int, _csobject:CSObject):
        self.__object:CSObject = _csobject
        self.__rcount:int      = 0
        self.__offset:int      = _offset
        self.__cleanl:bool     = False
    
    def cleanLast(self):
        """ HACK!!

            Foooocc!
        """
        self.__cleanl = True
    
    def safeClean(self):
        return not self.__cleanl
    
    def increment(self):
        self.__rcount += 1
    
    def decrement(self):
        self.__rcount -= 1
    
    def getObject(self):
        return self.__object
    
    def getRcount(self):
        return self.__rcount
    
    def getOffset(self):
        return self.__offset
    
    
    def __str__(self):
        return self.__object.toString().__str__()
    



class CSMemory:

    ALLOCATIONS:int = 0
    MEMORY:list[ObjectWrapper] = []

    @staticmethod
    def CSMalloc(_csobject:CSObject) -> ObjectWrapper:
        # ===== monitor alloc|
        # ===================|
        CSMemory.onAllocate()

        # ====== allocate new|
        # ===================|
        _offset = len(CSMemory.MEMORY)
        CSMemory.MEMORY.append(ObjectWrapper(_offset, _csobject))
        return CSMemory.MEMORY[-1]
    
    @staticmethod
    def getObjectAt(_index:int):
        return CSMemory.MEMORY[_index]

    @staticmethod
    def incrementAt(_index:int):
        if  _index != None:
            if  CSMemory.MEMORY[_index]:
                CSMemory.MEMORY[_index].increment()

    @staticmethod
    def decrementAt(_index:int):
        if  _index != None:
            if  CSMemory.MEMORY[_index]:
                CSMemory.MEMORY[_index].decrement()

    @staticmethod
    def onAllocate():
        CSMemory.ALLOCATIONS += 1

        # run every 500 or over allocation
        if  CSMemory.ALLOCATIONS >= 500:
            from cscriptvm.csvm import CSVirtualMachine as VM
            if  VM.isrunning():
                CSMemory.collect()
                del VM
            # not running vm|reset
            CSMemory.ALLOCATIONS = 0

    @staticmethod
    def collect():
        _collected = 0
        for idx in range(len(CSMemory.MEMORY)):
            if  CSMemory.MEMORY[idx] != None:
                if  CSMemory.MEMORY[idx].getRcount() <= 0 and CSMemory.MEMORY[idx].safeClean():
                    CSMemory.MEMORY[idx] = None
                    _collected += 1
        
        return _collected
    
    @staticmethod
    def collectForce():
        _collected = 0
        for idx in range(len(CSMemory.MEMORY)):
            if  CSMemory.MEMORY[idx] != None:
                if  CSMemory.MEMORY[idx].getRcount() <= 0:
                    CSMemory.MEMORY[idx] = None
                    _collected += 1
        
        return _collected
    
    @staticmethod
    def collectdump():
        _collected = CSMemory.collectForce()
        print("GarbageCollected: %d" % _collected)
        
        _memory = []
        for i in CSMemory.MEMORY:
            if  i:
                if  i.getRcount() > 0:
                    _memory.append(i.getObject().toString().__str__())
        print("Mem:", _memory)
        