
import dis


code ="""
x = False
if  x and False:
    print
else:
    2 + 2
"""
dis.dis(code)