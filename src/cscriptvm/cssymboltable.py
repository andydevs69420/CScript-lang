


class Node(object):
    """ 
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.data = ({
            # data here!
        })
    
    def insert(self, _symbol:str, **_props:dict):
        if  self.lookup(_symbol):
            return self.lookup(_symbol)
        # insert
        self.data[_symbol] = _props
    
    def vlocal(self, _symbol:str):
        return (_symbol in self.data.keys())

    def lookup(self, _symbol:str):
        if  (_symbol in self.data.keys()):
            return self.data[_symbol]
        
        _parent = self.head
        while _parent:
            if  _parent.lookup(_symbol):
                return _parent\
                .lookup(_symbol)
            _parent = _parent.head
        return  False



class CSSymbolTable:

    CURRENT = None
    HISTORY = []

    @staticmethod
    def insert(_symbol:str, **_props:dict):
        assert CSSymbolTable.CURRENT, "empty scope!"
        return CSSymbolTable.CURRENT.insert(_symbol, **_props)

    @staticmethod
    def exists(_symbol:str):
        if  not CSSymbolTable.CURRENT:
            return False
        return (True if CSSymbolTable.CURRENT.lookup(_symbol) else False)
    
    @staticmethod
    def islocal(_symbol:str):
        assert CSSymbolTable.CURRENT, "empty scope!"
        return CSSymbolTable.CURRENT.vlocal(_symbol)
    
    @staticmethod
    def newScope():
        if  not CSSymbolTable.CURRENT:
            CSSymbolTable.CURRENT = Node()
            return
        
        # append history
        _old:Node = CSSymbolTable.CURRENT
        _new:Node = Node()

        _old.tail = _new
        _new.head = _old

        CSSymbolTable.CURRENT = _new
        CSSymbolTable.HISTORY.append(_old)

    @staticmethod
    def endScope():
        if  len(CSSymbolTable.HISTORY) <= 0:
            CSSymbolTable.CURRENT = None
            return
        CSSymbolTable.CURRENT =  CSSymbolTable.HISTORY.pop()


