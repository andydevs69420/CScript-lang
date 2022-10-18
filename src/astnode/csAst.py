
# core
from cscriptvm.compilable import Compilable

class CSAst(Compilable):pass
class CSAst(Compilable):
    """ CSAst ast for cscript
    """

    def __init__(self):
        super().__init__()
        
    
    def compile(self):
        """ Compiles ast

            Returns
            -------
            None
        """
        raise NotImplementedError(f"{type(self).__name__}::compile method must be override!")

    def isOverloading(self):
        return False

    def isAssignable(self):
        return False
    
    def isMemberAssignable(self):
        return False
    
    def assignTo(self):
        """ Fires when simple assignment and augmented assignment

            Example
            -------
            x =  2
            x += 2
        """
        raise NotImplementedError(f"{type(self).__name__}::assignTo method must be overritten!")

    def evaluate(self):
        """ Leave None!!!
        """
        return None