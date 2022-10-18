
from csAst import CSAst


class SpitsCode(CSAst):
    def __init__(self):
        super().__init__()
    
    def newSet(self):
        self.INSTRUCTIONS.append([])
    
    def popSet(self):
        return SpitsCode.INSTRUCTIONS.pop()
