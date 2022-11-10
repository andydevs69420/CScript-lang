

# deprecated: produces alot of collision
def hasher(_key:str):
    if isinstance(_key, int): return _key

    _key = str(_key)
    if  len(_key) <= 0: return 0

    _hashcode = 69420

    for char in _key:
        _hashcode  = ((_hashcode << 5) - _hashcode) + ord(char)
        _hashcode |= 0
    return _hashcode


class Node(object):

    def __init__(self, _key:str, _data):
        self.nkey = _key
        self.data = _data
        self.tail = None

class LinkedList(Node):
    
    def __init__(self, _key:str, _data):
        super().__init__(_key, _data)

    def append(self, _data:Node):
        
        _head = self
        _last = _head
        while _last:

            if _last.nkey == _data.nkey:
                # update
                _last.data = _data.data
                return 

            _head = _last
            _last = _last.tail

        _head.tail = _data
        return
    
    def __str__(self) :
        _count = 0
        _head = self

        while _head:
            _count += 1
            _head = _head.tail

        return "<LinkedList with %d node count/>" % _count



class HashMap(object):
    """ 
    """

    def walk(self, _key:str):
        for _ll in self.__bucket:
            if  _ll:
                _head = _ll
                while _head:
                    if  _head.nkey == _key:
                        return _head.data
                    
                    _head = _head.tail

        return _head

    def __init__(self):
        self.__nitems =  0
        self.__bcount = 16
        self.__bucket = [
            None for _ in range(self.__bcount)
        ]

        self.hidden = []
    
    def put(self, _key:str, _data:object):
        _bucket_index = hasher(_key) % self.__bcount
        if  self.__bucket[_bucket_index] != None:
            # collision | update
            return self.__bucket[_bucket_index].append(Node(_key, _data))
        # insert
        self.__bucket[_bucket_index] = LinkedList(_key, _data)
        self.__nitems += 1

        _load_factor = float(self.__nitems) / self.__bcount

        if _load_factor > 0.75:
            self.__rehash()
        
    def get(self, _key:str):
        _hashed_key = hasher(_key) % self.__bcount
        assert self.hasKey(_key), "key error: key '%s' not found!" % _key

        _head = self.__bucket[_hashed_key]

        while _head:
            if  _head.nkey == _key:
                return _head.data
            
            _head = _head.tail
        
        raise KeyError("'%s' key not found!" % _key)
        

    def __rehash(self):
        """ Rehashing when bucket is potential full

            :internal
        """
        # increase by mupltiply of 2 := 16 * 2 = 32
        self.__bcount *= 2
        self.__nitems = 0

        _copy = self.__bucket
        self.__bucket = [
            None for _ in range(self.__bcount)
        ]

        for node in _copy:
            if  node:
                last = node
                while last:
                    self.put(last.nkey, last.data)
                    last = last.tail

    def keys(self):
        """ Retrieve all keys
        """
        _keys = []
        for buck in self.__bucket:
            if  buck:
                _last = buck
                while _last:
                    _keys.append(_last.nkey)
                    _last = _last.tail
       
        return _keys
    
    def hasKey(self, _key:str):
        """ Checks if key exists
        """
        _bucket_index = hasher(_key) % self.__bcount
        if  self.__bucket[_bucket_index] == None:
            return False
        _head = self.__bucket[_bucket_index]
        while _head:
            if  _head.nkey == _key:
                return True
            _head = _head.tail
        return False
    
    def __str__(self):
        _keys   = self.keys()
        _attrib = ""
        for k in range(len(_keys)):
            _value  = self.get(_keys[k])
            _string = ...

            if  (self is _value):
                # refering to its self
                # to avoid recursion  
                _string = "{self}"
            else:
                _string = _value.__str__()

            if  _keys[k] not in self.hidden:
                _attrib += f"{_keys[k]}: {_string}"

                if  k < ((len(_keys) - 1) - len(self.hidden)):
                    _attrib += ", "

        return "{" + f"{_attrib}" + "}"

    



if  __name__ == "__main__":
    hashmap = HashMap()

    hashmap.put("andy", "Philipp")
    hashmap.put("Marielle", "Philipp2")
    hashmap.put("Philipp", "Marielle")

    print(hashmap.get("andy"))
    print(hashmap.get("Marielle"))
    print(hashmap.get("Philipp"))



    hashmap.put("self", hashmap)
    print(hashmap)
