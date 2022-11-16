
import dis


code = """

w = 1
x = [1,2,3, [4,5,w]]


"""

dis.dis(code)