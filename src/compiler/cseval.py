


from utility.asttypes import ExpressionType


class CSEval(object):

    def evaluate(self,_node:dict):
        match _node["type"]:
            case ExpressionType.INTEGER:
                return self.ev_integer(_node)
            case ExpressionType.DOUBLE:
                return self.ev_double(_node)
            case ExpressionType.STRING:
                return self.ev_string(_node)
            case ExpressionType.BOOLEAN:
                return self.ev_boolean(_node)
            case ExpressionType.NULL:
                return self.ev_null(_node)
            case ExpressionType.UNARY_EXPR:
                return self.ev_unary(_node)
            case ExpressionType.BINARY_EXPR:
                return self.ev_binary(_node)
            case ExpressionType.COMPARE_EXPR:
                return self.ev_compare(_node)
            case ExpressionType.LOGICAL_EXPR:
                return self.ev_logical(_node)
        # specify ellipsis return
        return ...
    
    # eval integer
    def ev_integer(self, _node:dict):
        return int(_node["const"])
    
    # eval double
    def ev_double(self, _node:dict):
        return float(_node["const"])
    
    # eval string
    def ev_string(self, _node:dict):
        return str(_node["const"])
    
    # eval boolean
    def ev_boolean(self, _node:dict):
        return bool(_node["const"] == "true")
    
    # eval null
    def ev_null(self, _node:dict):
        return float(_node["const"])

    # eval binary
    def ev_binary(self, _node:dict):
        _a = self.evaluate(_node["left" ])
        _b = self.evaluate(_node["right"])

        if  ((_a or _b) == ...):
            # specify ellipsis return
            return ...
        
        try:
            match _node["opt"]:
                case "^^":
                    return _a ** _b
                case '*':
                    return _a *  _b
                case '/':
                    return _a /  _b
                case '%':
                    return _a %  _b
                case '+':
                    return _a +  _b
                case '-':
                    return _a -  _b
                case "<<":
                    return _a << _b
                case ">>":
                    return _a >> _b
                case '&':
                    return _a &  _b
                case '^':
                    return _a ^  _b
                case '|':
                    return _a |  _b
        except TypeError:
            ...
        except ZeroDivisionError:
            ...

    # eval compare
    def ev_compare(self, _node:dict):
        _a = self.evaluate(_node["left" ])
        _b = self.evaluate(_node["right"])

        if  ((_a or _b) == ...):
            # specify ellipsis return
            return ...
        
        try:
            match _node["opt"]:
                case '<':
                    return _a <  _b
                case "<=":
                    return _a <= _b
                case '>':
                    return _a >  _b
                case ">=":
                    return _a >= _b
                case "==":
                    return _a == _b
                case "!=":
                    return _a != _b
        except TypeError:
            ...
    
    def ev_logical(self, _node:dict):
        _a = self.evaluate(_node["left" ])
        _b = self.evaluate(_node["right"])

        if  ((_a or _b) == ...):
            # specify ellipsis return
            return ...

        match _node["opt"]:
            case "&&":
                return _a and _b
            case "||" :
                return _a or  _b