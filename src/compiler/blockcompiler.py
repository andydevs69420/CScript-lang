


# .
from .compilable import Compilable

# utility
from utility import ExpressionType, SyntaxType

TYPE= "type"

class BlockCompiler(Compilable):
    """ Basic Block compiler
    """

    def __init__(self):
        super().__init__()
    
    def visit(self, _node:dict):
        match _node[TYPE]:
            case ExpressionType.VARIABLE:
                return self.cvariable(_node)
            case ExpressionType.INTEGER:
                return self.cinteger(_node)
            case ExpressionType.DOUBLE:
                return self.cdouble(_node)
            case ExpressionType.STRING:
                return self.cstring(_node)
            case ExpressionType.BOOLEAN:
                return self.cboolean(_node)
            case ExpressionType.NULL:
                return self.cnull(_node)
            case ExpressionType.THIS:
                return self.cthis(_node)
            case ExpressionType.FUNCTION_EXPR:
                return self.cfuncexpr(_node)
            case ExpressionType.ARRAY:
                return self.carray(_node)
            case ExpressionType.OBJECT:
                return self.cobject(_node)
            case ExpressionType.ALLOCATION:
                return self.callocation(_node)
            case ExpressionType.STATIC_MEMBER:
                return self.cstaticmember(_node)
            case ExpressionType.MEMBER:
                return self.cmember(_node)
            case ExpressionType.SUBSCRIPT:
                return self.csubscript(_node)
            case ExpressionType.CALL:
                return self.ccall(_node)
            case ExpressionType.POSTIFIX_EXPR:
                return self.cpostfix(_node)
            case ExpressionType.UNARY_EXPR:
                return self.cunary(_node)
            case ExpressionType.BINARY_EXPR:
                return self.cbinary(_node)
            case ExpressionType.COMPARE_EXPR:
                return self.ccompare(_node)
            case ExpressionType.LOGICAL_EXPR:
                return self.clogical(_node)
            case ExpressionType.TERNARY_EXPR:
                return self.cternary(_node)
            case ExpressionType.ASSIGNMENT_EXPR:
                return self.cassignment(_node)
            case ExpressionType.AUGMENTED_EXPR:
                return self.caugmented(_node)
            # =========== statement|
            # =====================|
            case SyntaxType.CLASS_DEC:
                return self.cclass(_node)
            case SyntaxType.VAL_STMNT:
                return self.cvaldec(_node)
            case SyntaxType.CLASS_FUNC_DEC:
                return self.cclassfunc(_node)
            case SyntaxType.FUNC_DEC:
                return self.cfunc(_node)
            case SyntaxType.IF_STMNT:
                return self.cifstmnt(_node)
            case SyntaxType.WHILE_STMNT:
                return self.cwhile(_node)
            case SyntaxType.DO_WHILE_STMNT:
                return self.cdowhile(_node)
            case SyntaxType.SWITCH_STMNT:
                return self.cswitch(_node)
            case SyntaxType.TRY_EXCEPT:
                return self.ctryexcept(_node)
            case SyntaxType.BLOCK:
                return self.cblock(_node)
            case SyntaxType.IMPORT_STMNT:
                return self.cimport(_node)
            case SyntaxType.VAR_STMNT:
                return self.cvardec(_node)
            case SyntaxType.LET_STMNT:
                return self.cletdec(_node)
            case SyntaxType.THROW_STMNT:
                return self.cthrow(_node)
            case SyntaxType.ASSERT_STMNT:
                return self.cassert(_node)
            case SyntaxType.BREAK_STMNT:
                return self.cbreak(_node)
            case SyntaxType.CONTINUE_STMNT:
                return self.ccontinue(_node)
            case SyntaxType.RETURN_STMNT:
                return self.creturn(_node)
            case SyntaxType.PRINT_STMNT:
                return self.cprint(_node)
            case SyntaxType.PRINT_STMNT:
                return self.cprint(_node)
            case SyntaxType.EXPRESSION_STMNT:
                return self.cexpression(_node)
            case SyntaxType.MODULE:
                return self.cmodule(_node)

        raise TypeError("invalid ast type %d" % _node[TYPE])

    def compile(self):
        raise NotImplementedError(f"{type(self).__name__}::compile must be overritten!")