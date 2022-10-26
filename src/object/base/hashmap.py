
from strongtyping.strong_typing import match_typing


@match_typing
def hasher(_key:str):
    _key = str(_key)
    
    if  len(_key) <= 0: return 0

    _hashcode = 0
    for char in _key:
        _hashcode = ((_hashcode << 5) - _hashcode) + ord(char)
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
        
        _last = self
        while _last:

            if _last.nkey == _data.nkey:
                # update
                _last.data = _data.data
                return 

            _last = _last.tail

        self.tail = _data
        return






class HashMap(object):
    def __init__(self):
        self.nitems = 0
        self.bcount = 16
        self.bucket = [
            None for _ in range(self.bcount)
        ]
    
    def put(self, _key:str, _data):
        
        _bucket_index = hasher(_key) % self.bcount

        if  self.bucket[_bucket_index] != None:
            # collision | update
            return self.bucket[_bucket_index].append(Node(_key, _data))
        
        # insert
        self.bucket[_bucket_index] = LinkedList(_key, _data)
        self.nitems += 1

        _load_factor = float(self.nitems) / self.bcount

        if _load_factor > 0.75:
            self.rehash()
        
    def get(self, _key:str):
        _hashed_key = hasher(_key) % self.bcount
        assert self.bucket[_hashed_key] != None, "key error: key '%s' not found!" % _key

        _head = self.bucket[_hashed_key]

        while _head:
            if  _head.nkey == _key:
                return _head.data
            
            _head = _head.tail
        
        raise KeyError("'%s' key not found!" % _key)
        

    def rehash(self):
        # increase by mupltiply of 2 := 16 * 2 = 32
        self.bcount *= 2
        self.copy = self.bucket
        self.bucket = [
            None for _ in range(self.bcount)
        ]

        for node in self.bucket:
            if  node != None:
                last = node
                while last:
                    self.put(last.nkey, last.data)
                    last = last.tail


    def keys(self):
        _keys = []
        for buck in self.bucket:
            if  buck:
                _last = buck
                while _last:
                    _keys.append(_last.nkey)
                    _last = _last.tail
        
        return _keys
    


if  __name__ == "__main__":
    hashmap = HashMap()

    hashmap.put("andy", "Philipp")
    hashmap.put("Marielle", "Philipp2")
    hashmap.put("Philipp", "Marielle")

    print(hashmap.get("andy"))
    print(hashmap.get("Marielle"))
    print(hashmap.get("Philipp"))
