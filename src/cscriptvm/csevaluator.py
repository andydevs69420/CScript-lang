
"""
    Compile time evaluator.
    For code optimization purposes!

    author: andydevs69420
"""

# ======= global|
# ==============|
from cstoken import CSToken
# ========== end|

class Evaluatable(object):pass
class Evaluator(object):pass

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


class Evaluator(object):
    """ Arithmetic Node Evaluator
    """

    @staticmethod
    def evaluate_ternary_op(_condition:Evaluatable|Evaluator, _true:Evaluatable|Evaluator, _false:Evaluatable|Evaluator):
        
        if  not(isinstance(_condition, (Evaluatable, Evaluator)) and (isinstance(_true, (Evaluatable, Evaluator)), isinstance(_false, (Evaluatable, Evaluator)))):
            return None

        _cond = _condition.evaluate()
        if  _cond:
            if  _cond.get("this"):
                return _true.evaluate()
            else:
                return _false.evaluate()
        
        return None


    @staticmethod
    def evaluate_unary_op(_opt:CSToken, _rhs:Evaluatable|Evaluator):

        if  not isinstance(_rhs, (Evaluatable, Evaluator)):
            return None
        
        _rhs = _rhs.evaluate()
        if  not _rhs: return _rhs

        if _opt.matches("~"):
            return _rhs.bit_not(_opt, _allocate=False)
        elif _opt.matches("!"):
            return _rhs.bin_not(_opt, _allocate=False)
        elif _opt.matches("+"):
            return _rhs.positive(_opt, _allocate=False)
        elif _opt.matches("-"):
            return _rhs.negative(_opt, _allocate=False)
        
        raise ValueError("invalid unary op value \"%s\"" % _opt)

    @staticmethod
    def evaluate_bin_op(_opt:CSToken, _lhs:Evaluatable|Evaluator, _rhs:Evaluatable|Evaluator):
        if  not(isinstance(_lhs, (Evaluatable, Evaluator)) and isinstance(_rhs, (Evaluatable, Evaluator))):
            return None

        _lhs = _lhs.evaluate()
        _rhs = _rhs.evaluate()

        if not (_lhs and _rhs):\
        return None

        if _opt.matches("^^"):
            return _lhs.pow(_opt, _rhs, _allocate=False)
        elif _opt.matches('*'):
            return _lhs.mul(_opt, _rhs, _allocate=False)
        elif _opt.matches('/'):
            return _lhs.div(_opt, _rhs, _allocate=False)
        elif _opt.matches('%'):
            return _lhs.mod(_opt, _rhs, _allocate=False)
        elif _opt.matches('+'):
            return _lhs.add(_opt, _rhs, _allocate=False)
        elif _opt.matches('-'):
            return _lhs.sub(_opt, _rhs, _allocate=False)
        elif _opt.matches("<<"):
            return _lhs.lshift(_opt, _rhs, _allocate=False)
        elif _opt.matches(">>"):
            return _lhs.rshift(_opt, _rhs, _allocate=False)
        elif _opt.matches('&'):
            return _lhs.bit_and(_opt, _rhs, _allocate=False)
        elif _opt.matches('^'):
            return _lhs.bit_xor(_opt, _rhs, _allocate=False)
        elif _opt.matches('|'):
            return _lhs.bit_or(_opt, _rhs, _allocate=False)

        raise ValueError("invalid binary op value \"%s\"" % _opt)

    @staticmethod
    def evaluate_comp_op(_opt:CSToken, _lhs:Evaluatable|Evaluator, _rhs:Evaluatable|Evaluator):

        if  not(isinstance(_lhs, (Evaluatable, Evaluator)) and isinstance(_rhs, (Evaluatable, Evaluator))):
            return None

        _lhs = _lhs.evaluate()
        _rhs = _rhs.evaluate()

        if not (_lhs and _rhs):\
        return None

        if _opt.matches('<'):
            return _lhs.lt(_opt, _rhs, _allocate=False)
        elif _opt.matches("<="):
            return _lhs.lte(_opt, _rhs, _allocate=False)
        elif _opt.matches('>'):
            return _lhs.gt(_opt, _rhs, _allocate=False)
        elif _opt.matches(">="):
            return _lhs.gte(_opt, _rhs, _allocate=False)
        elif _opt.matches("=="):
            return _lhs.eq(_opt, _rhs, _allocate=False)
        elif _opt.matches("!="):
            return _lhs.neq(_opt, _rhs, _allocate=False)
        elif _opt.matches("&&"):
            return _lhs.log_and(_opt, _rhs, _allocate=False)
        elif _opt.matches("||"):
            return _lhs.log_or(_opt, _rhs, _allocate=False)

        raise ValueError("invalid compare op value \"%s\"" % _opt)