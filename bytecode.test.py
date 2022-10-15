
import dis


code ="""
a = 10

match a:
    case 10, 20:
        print("yes")
    case 30, 40:
        print("no")

"""
dis.dis(code)