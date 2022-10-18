from object.csobject import CSObject



"""
    Only those objects that are being used by a variable are stored here :(
        anything else will be consider as garbage
"""

class CSMemoryAddress(object):
    """ CSMemoryAddress
    """ 

    def __init__(self, _addres:int):
        self.__address:int = _addres
        self.__refsize:int = 0
    
    def getAddress(self):
        """ Returns address|index

            Returns
            -------
            int
        """
        return self.__address
    
    def getRefsize(self):
        """ Returns object reference count

            Returns
            -------
            int
        """
        return self.__refsize
    
    def increment(self):
        """ Increments refcount

            Returns
            -------
            None
        """
        self.__refsize += 1
    
    def decrement(self):
        """ Decrements refcount

            Returns
            -------
            None
        """
        self.__refsize -= 1
    
    def __str__(self):
        return f"address:{hex(self.__address)}, refsize:{self.__refsize}"



class GarbageCollector(object):

    def __init__(self):
        self.allocations:int = 0
    
    def onallocate(self):
        raise NotImplementedError("GarbageCollector::onallocate needs to be overriten!")

    def collect(self):
        raise NotImplementedError("GarbageCollector::collect needs to be overriten!")


class CSMemory(GarbageCollector):
    """ CSMemory
    """
    def __init__(self):
        super().__init__()
        self.__model:list[CSObject] = []
        self.__oaddr:list[CSMemoryAddress] = []
        self.__refpt:dict[int: CSMemoryAddress] = ({
            # 
        })
    
    def alloc(self, _csobj:CSObject) -> CSMemoryAddress:
        self.onallocate()
        self.__model.append(_csobj)

        _ref_index = len(self.__refpt)

        self.__oaddr.append(CSMemoryAddress(len(self.__model)-1))
        self.__refpt[_ref_index] = (len(self.__oaddr) - 1)
        return _ref_index
    
    def makeObject(self, _csobj:CSObject) -> CSMemoryAddress:
        self.onallocate()
        self.__model.append(_csobj)
        self.__oaddr.append(CSMemoryAddress(len(self.__model)-1))
        return (len(self.__oaddr) - 1)
    
    def initializeToName(self, _old:int) -> int:
        _new_location = self.alloc(CSObject.new_nulltype("null"))
        self.__oaddr[self.__refpt[_old]].increment()
        return _new_location
    
    def setToName(self, _old:int, _new:int):
        if _old == _new: return
        if  self.__oaddr[self.__refpt[_old]] != None:
            # possiby deleted by garbage
            self.__oaddr[self.__refpt[_old]].decrement()
        self.__refpt[_old] = self.__refpt[_new]
        self.__oaddr[self.__refpt[_new]].increment()
    
    def setToObject(self, _old:int, _object_address_index:int):
        if  self.__oaddr[self.__refpt[_old]] != None:
            # possiby deleted by garbage
            self.__oaddr[self.__refpt[_old]].decrement()
        self.__refpt[_old] = _object_address_index
        self.__oaddr[_object_address_index].increment()
    
    def getAddress(self, _address:int) -> CSMemoryAddress:
        return self.__oaddr[self.__refpt[_address]]

    def incrementAt(self, _address:int):
        return self.__oaddr[self.__refpt[_address]].increment()

    def getCSObject(self, _address:int) -> CSObject:
        return self.__model[self.__oaddr[self.__refpt[_address]].getAddress()]
    
    def onallocate(self):
        # runs garbage collector on every 1000 allcation
        self.allocations += 1
        if  self.allocations >= 1000:
            self.allocations = 0
            self.collect()

    def collect(self):
        _index = 0
        for each_obj_addr in self.__oaddr:
            
            if  each_obj_addr != None:
                if  each_obj_addr.getRefsize() <= 0:
                    self.__model[each_obj_addr.getAddress()] = None
                    self.__oaddr[_index] = None
            _index += 1

    def dump(self):
        self.__dump__model()
        self.__dump__address()

    def __dump__model(self):
        print("model len: %d" % len([*filter(lambda x: x != None, self.__model)]))
        print([*filter(lambda x: x != None, self.__model)])


    def __dump__address(self):
        print("address len: %d" % len([*filter(lambda x: x != None, self.__oaddr)]))
        for each_addr in self.__oaddr:
            if  each_addr != None:
                print(each_addr.__str__(), "object ->", self.__model[each_addr.getAddress()].toString().__str__())
