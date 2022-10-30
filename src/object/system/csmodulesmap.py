



from non_primitive.csmap import CSMap


class CSModulesMap(CSMap):
    def __init__(self):
        super().__init__()
    
    def contains(self, _key:str):
        return self.thiso.hasKey(_key)
    
