# ==========global|
# ================|
from grammarp.cstoken import CSToken
# ============ end|



# =========== core|
# ================|
from cscriptvm.csvm import CSVM as VM
from cscriptvm.cssymboltable2 import ST
from cscriptvm.csevaluator import Evaluatable, Evaluator
# ============ end|


# ========= object|
# ================|
from base.csobject import CSObject
# ============ end|

from astnode.utils.compilable import Compilable



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
    
    def isBreak(self):
        """ Determine if the ast is "break statement"
        """
        return False

    def isContinue(self):
        """ Determine if the ast is "continue statement"
        """
        return False