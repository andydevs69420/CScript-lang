
class Table(object):pass
class Table(object):

    def __init__(self, _parent=None):
        self.parent = _parent
        self.symbols = ({})

    # operations
    def existsglobally(self, _symbol:str):
        if  (self.existslocally(_symbol)): return True
        
        _parent = self.parent
        while _parent:
            if  _parent.existsglobally(_symbol):
                return True
            _parent = _parent.parent

        return False

    def existslocally(self, _symbol:str):
        return (_symbol in self.symbols.keys())

    def lookup(self, _symbol:str):
        if  self.existslocally(_symbol):
            return self.symbols[_symbol]
        
        _parent = self.parent
        while _parent:
            _info = _parent.lookup(_symbol)
            if  _info:
                return _info
            
            _parent = _parent.parent
        
        return False
    
    def insert(self, _symbol:str, **_props):
        if  self.existslocally(_symbol):
            return self.symbols[_symbol]
        self.symbols[_symbol] = _props

    def setParent(self, _node:Table):
        self.parent = _node

class ST:
    def __init__(self):
        self.globaltable:Table = Table(None)
        self.current = self.globaltable
        self.__stack = []

    def newScope(self):
        self.__stack.append(Table(self.current))
        self.current:Table = self.__stack[-1]
    
    def endScope(self):
        self.current:Table = self.__stack.pop()

        if  len(self.__stack) <= 0:
            self.current = self.globaltable



if  __name__ == "__main__":
    _stable = ST()

    _stable.globaltable.insert("var_x", _loc=1)
    _stable.globaltable.insert("var_y", _loc=2)
    print(_stable.globaltable.existslocally("var_x"))
    print(_stable.globaltable.existslocally("var_y"))

    _stable.localstable.insert("local", _loc=2)

    _stable.newScope() # 1
    _stable.newScope()      # 2
    _stable.current.insert("var_y")
    print(_stable.current.existsglobally("var_y"))
    print(_stable.current.existslocally ("var_y"))
    _stable.endScope()      # 2
    _stable.endScope() # 1

    print(_stable.current.existslocally("local"))
        

