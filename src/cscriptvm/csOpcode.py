



from enum import Enum


class CSOpCode(Enum):

   PUSH_CONST = 0x00

   BINARY_POW = 0x02
   BINARY_MUL = 0x03
   BINARY_DIV = 0x04
   BINARY_MOD = 0x05
   BINARY_ADD = 0x06
   BINARY_SUB = 0x07
   BINARY_LSHIFT = 0x08
   BINARY_RSHIFT = 0x09
   BINARY_AND = 0x0a
   BINARY_XOR = 0x0b
   BINARY_OR  = 0x0c
