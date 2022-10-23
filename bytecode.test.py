
import dis


code = """

x = [1,2,3,4]

x[0] = 2

"""
dis.dis(code)