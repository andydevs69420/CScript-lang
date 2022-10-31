
import dis


code = """

vv ="www"

class Animal:

    x = 2

    def eat():
        print("Yumm!")

"""

dis.dis(code)