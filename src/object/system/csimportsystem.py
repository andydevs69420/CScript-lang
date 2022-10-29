

class ImportTable(object):

    def __init__(self, _name:str):
        self.parent = None
        self.name = _name
        self.imports = ({
            # name: CSModule object
        })
    
    def insert(self, _name:str, _node):
        self.imports[_name]


class ImportSystem(object):

    def __init__(self):
        self.root = ImportTable("/")
    
    def newImport(self, _name:str):
        self.root.insert(_name, ImportTable(_name))

