
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
        

        if _opt.matches("~"):
            return _rhs.evaluate().bit_not(_opt)
        elif _opt.matches("!"):
            return _rhs.evaluate().bin_not(_opt)
        elif _opt.matches("+"):
            return _rhs.evaluate().positive(_opt)
        elif _opt.matches("-"):
            return _rhs.evaluate().negative(_opt)
        
        raise ValueError("invalid unary op value \"%s\"" % _opt)

    @staticmethod
    def evaluate_bin_op(_opt:CSToken, _lhs:Evaluatable|Evaluator, _rhs:Evaluatable|Evaluator):

        if  not(isinstance(_lhs, (Evaluatable, Evaluator)) and isinstance(_rhs, (Evaluatable, Evaluator))):
            return None

        if _opt.matches("^^"):
            return _lhs.evaluate()\
                .pow(_opt, _rhs.evaluate())
        elif _opt.matches('*'):
            return _lhs.evaluate()\
                .mul(_opt, _rhs.evaluate())
        elif _opt.matches('/'):
            return _lhs.evaluate()\
                .div(_opt, _rhs.evaluate())
        elif _opt.matches('%'):
            return _lhs.evaluate()\
                .mod(_opt, _rhs.evaluate())
        elif _opt.matches('+'):
            return _lhs.evaluate()\
                .add(_opt, _rhs.evaluate())
        elif _opt.matches('-'):
            return _lhs.evaluate()\
                .sub(_opt, _rhs.evaluate())
        elif _opt.matches("<<"):
            return _lhs.evaluate()\
                .lshift(_opt, _rhs.evaluate())
        elif _opt.matches(">>"):
            return _lhs.evaluate()\
                .rshift(_opt, _rhs.evaluate())
        elif _opt.matches('&'):
            return _lhs.evaluate()\
                .bit_and(_opt, _rhs.evaluate())
        elif _opt.matches('^'):
            return _lhs.evaluate()\
                .bit_xor(_opt, _rhs.evaluate())
        elif _opt.matches('|'):
            return _lhs.evaluate()\
                .bit_or(_opt, _rhs.evaluate())

        raise ValueError("invalid binary op value \"%s\"" % _opt)

    @staticmethod
    def evaluate_comp_op(_opt:CSToken, _lhs:Evaluatable|Evaluator, _rhs:Evaluatable|Evaluator):

        if  not(isinstance(_lhs, (Evaluatable, Evaluator)) and isinstance(_rhs, (Evaluatable, Evaluator))):
            return None

        if _opt.matches('<'):
            return _lhs.evaluate()\
                .lt(_opt, _rhs.evaluate())
        elif _opt.matches("<="):
            return _lhs.evaluate()\
                .lte(_opt, _rhs.evaluate())
        elif _opt.matches('>'):
            return _lhs.evaluate()\
                .gt(_opt, _rhs.evaluate())
        elif _opt.matches(">="):
            return _lhs.evaluate()\
                .gte(_opt, _rhs.evaluate())
        elif _opt.matches("=="):
            return _lhs.evaluate()\
                .eq(_opt, _rhs.evaluate())
        elif _opt.matches("!="):
            return _lhs.evaluate()\
                .neq(_opt, _rhs.evaluate())
        elif _opt.matches("&&"):
            return _lhs.evaluate()\
                .log_and(_opt, _rhs.evaluate())
        elif _opt.matches("||"):
            return _lhs.evaluate()\
                .log_or(_opt, _rhs.evaluate())

        raise ValueError("invalid compare op value \"%s\"" % _opt)