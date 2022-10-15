
import dis


code = """

a = [1,2,3,4,5,6]
b = a

a = 2
c = 2

"""
dis.dis(code)