
import dis


code = """
x = 0

import math

while x < 10:
    if x == 5: continue
    print("x =", x)
    x += 1

import math
"""

dis.dis(code)