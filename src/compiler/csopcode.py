from enum import Enum
class CSOpCode(Enum):

   LOAD_MODULE = 1
   PUSH_INTEGER = 2
   PUSH_DOUBLE  = 3
   PUSH_STRING = 4
   PUSH_BOOLEAN = 5
   PUSH_NULL = 6
   THIS_OP  = 600
   PUSH_OBJECT = 7
   PUSH_CODE   = 8
   PUSH_NAME  = 9
   PUSH_LOCAL  = 10
   PUSH_CONST = 11
   MAKE_ARRAY = 12
   MAKE_OBJECT = 13
   MAKE_CLASS  = 14
   MAKE_FUNCTION  = 15
   MAKE_MODULE = 16
   GET_ATTRIB  = 17
   GET_METHOD  = 18
   SET_ATTRIB  = 19
   MAKE_VAR    = 20
   STORE_NAME  = 21
   MAKE_LOCAL  = 22
   STORE_LOCAL = 23
   CALL       = 24
   CALL_METHOD = 25
   POSTFIX_OP   = 26
   UNARY_OP   = 27
   BINARY_POW = 28
   BINARY_MUL = 29
   BINARY_DIV = 30
   BINARY_MOD = 31
   BINARY_ADD = 32
   BINARY_SUB = 33
   BINARY_LSHIFT = 34
   BINARY_RSHIFT = 35
   BINARY_AND = 36
   BINARY_XOR = 37
   BINARY_OR  = 38
   BINARY_SUBSCRIPT = 39
   SET_SUBSCRIPT = 40
   COMPARE_OP = 41

   INPLACE_POW = 42
   INPLACE_MUL = 43
   INPLACE_DIV = 44
   INPLACE_MOD = 45
   INPLACE_ADD = 46
   INPLACE_SUB = 47
   INPLACE_LSHIFT = 46
   INPLACE_RSHIFT = 49
   INPLACE_AND = 50
   INPLACE_XOR = 51
   INPLACE_OR = 52

   POP_JUMP_IF_FALSE = 53
   POP_JUMP_IF_TRUE = 54
   JUMP_IF_FALSE_OR_POP = 55
   JUMP_IF_TRUE_OR_POP = 56
   JUMP_NOT_EQUAL = 57
   JUMP_EQUAL = 58
   JUMP_TO = 59
   ABSOLUTE_JUMP = 60

   SETUP_TRY = 61
   POP_TRY = 62

   THROW_ERROR   = 63
   PRINT_OBJECT = 64
   DUP_TOP = 65
   POP_TOP = 66
   NEW_BLOCK = 67
   END_BLOCK = 68
   NO_OPERATION = 69
   RETURN_OP = 70