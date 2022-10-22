""" Ast that handles expression
"""


from astnode.globalast.cscodeblock import CodeBlock
from .csAst import CSAst, CSToken


# ========= core|
# ==============|
from cscriptvm.csevaluator import Evaluatable, Evaluator
# ===========end|


class ExpressionAst(CSAst, Evaluatable, Evaluator):pass
class ExpressionAst(CSAst, Evaluatable, Evaluator):

    def __init__(self):
        super().__init__()
    
    def islogical(self):
        """ Checks if logical exoression
        """
        return False

    def assignTo(self, _block:CodeBlock, _opt:CSToken):
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

