
import dis


code = """

x = 0

while x < 10:
    if x == 5: continue
    print("x =", x)
    x += 1
"""
dis.dis(code)

x = 0
while x < 10:
    if x == 5: continue
    print("x = ", x)
    x += 1
