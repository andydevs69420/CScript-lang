
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
    def evaluate_ternary_op(_condition:Evaluatable|Evaluator, _true:Evaluatable|Evaluator, _false:Evaluatable|Evaluator):
        
        if  not(isinstance(_condition, (Evaluatable, Evaluator)) and (isinstance(_true, (Evaluatable, Evaluator)), isinstance(_false, (Evaluatable, Evaluator)))):
            return None

        _cond = _condition.evaluate()
        if  _cond:
            if  _cond.getObject().get("this"):
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
            return _rhs.getObject().bit_not(_opt)
        elif _opt.matches("!"):
            return _rhs.getObject().bin_not(_opt)
        elif _opt.matches("+"):
            return _rhs.getObject().positive(_opt)
        elif _opt.matches("-"):
            return _rhs.getObject().negative(_opt)
        
        raise ValueError("invalid unary op value \"%s\"" % _opt)

    @staticmethod
    def evaluate_bin_op(_opt:CSToken, _lhs:Evaluatable|Evaluator, _rhs:Evaluatable|Evaluator):
        if  not(isinstance(_lhs, (Evaluatable, Evaluator)) and isinstance(_rhs, (Evaluatable, Evaluator))):
            return None

        print("called!")

        _lhs = _lhs.evaluate()
        _rhs = _rhs.evaluate()

        if not (_lhs and _rhs):\
        return None

        if _opt.matches("^^"):
            return _lhs.getObject().pow(_opt, _rhs.getObject())
        elif _opt.matches('*'):
            return _lhs.getObject().mul(_opt, _rhs.getObject())
        elif _opt.matches('/'):
            return _lhs.getObject().div(_opt, _rhs.getObject())
        elif _opt.matches('%'):
            return _lhs.getObject().mod(_opt, _rhs.getObject())
        elif _opt.matches('+'):
            return _lhs.getObject().add(_opt, _rhs.getObject())
        elif _opt.matches('-'):
            return _lhs.getObject().sub(_opt, _rhs.getObject())
        elif _opt.matches("<<"):
            return _lhs.getObject().lshift(_opt, _rhs.getObject())
        elif _opt.matches(">>"):
            return _lhs.getObject().rshift(_opt, _rhs.getObject())
        elif _opt.matches('&'):
            return _lhs.getObject().bit_and(_opt, _rhs.getObject())
        elif _opt.matches('^'):
            return _lhs.getObject().bit_xor(_opt, _rhs.getObject())
        elif _opt.matches('|'):
            return _lhs.getObject().bit_or(_opt, _rhs.getObject())

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
            return _lhs.getObject().lt(_opt, _rhs.getObject())
        elif _opt.matches("<="):
            return _lhs.getObject().lte(_opt, _rhs.getObject())
        elif _opt.matches('>'):
            return _lhs.getObject().gt(_opt, _rhs.getObject())
        elif _opt.matches(">="):
            return _lhs.getObject().gte(_opt, _rhs.getObject())
        elif _opt.matches("=="):
            return _lhs.getObject().eq(_opt, _rhs.getObject())
        elif _opt.matches("!="):
            return _lhs.getObject().neq(_opt, _rhs.getObject())
        elif _opt.matches("&&"):
            return _lhs.getObject().log_and(_opt, _rhs.getObject())
        elif _opt.matches("||"):
            return _lhs.getObject().log_or(_opt, _rhs.getObject())

        raise ValueError("invalid compare op value \"%s\"" % _opt)