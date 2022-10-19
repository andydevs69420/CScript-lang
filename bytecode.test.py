
import dis


code = """

try:

    2 + "Hola!";

except Exception as e:
    print(e)

"""
dis.dis(code)