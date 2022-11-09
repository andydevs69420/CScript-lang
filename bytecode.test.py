
import dis


code = """


class Dog:

    def cat(self):print



x = Dog()

x.cat()


"""

dis.dis(code)