
"""
    Compile time evaluator!
"""
from cstoken import CSToken

class Evaluatable(object):
    """ Interface for evaluatable node
    """

    def evaluate(self):
        """ Coverts data

            Returns
            -------
            pytype
        """
        raise NotImplementedError("evaluate method must be overitten!")


class Evaluator(object):pass
class Evaluator(object):
    """ Arithmetic Node Evaluator
    """

    @staticmethod
    def evaluate_unary_op(_opt:CSToken, _rhs:Evaluatable|Evaluator):

        if  not isinstance(_rhs, (Evaluatable, Evaluator)):
            return None
        
        _opt = _opt.token
        _rhs = _rhs.evaluate()

        if _opt == "~":
            return _rhs.bit_not()
        elif _opt == "!":
            return _rhs.bin_not()
        elif _opt == "+":
            return _rhs.positive()
        elif _opt == "-":
            return _rhs.negative()
        
        raise ValueError("invalid unary op value \"%s\"" % _opt)

    @staticmethod
    def evaluate_bin_op(_opt:CSToken, _lhs:Evaluatable|Evaluator, _rhs:Evaluatable|Evaluator):

        if  not(isinstance(_lhs, (Evaluatable, Evaluator)) and isinstance(_rhs, (Evaluatable, Evaluator))):
            return None

        _opt = _opt.token
        _lhs = _lhs.evaluate()
        _rhs = _rhs.evaluate()

        if _opt == "^^":
            return _lhs.pow(_rhs)
        elif _opt == '*':
            return _lhs.mul(_rhs)
        elif _opt == '/':
            return _lhs.div(_rhs)
        elif _opt == '%':
            return _lhs.mod(_rhs)
        elif _opt == '+':
            return _lhs.add(_rhs)
        elif _opt == '-':
            return _lhs.sub(_rhs)
        elif _opt == '&':
            return _lhs.bit_and(_rhs)
        elif _opt == '^':
            return _lhs.bit_xor(_rhs)
        elif _opt == '|':
            return _lhs.bit_or(_rhs)

        raise ValueError("invalid binary op value \"%s\"" % _opt)