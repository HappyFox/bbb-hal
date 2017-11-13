import os
import sys


if __name__ == "__main__":
    if os.getuid() != 0:
        print("Must run as root!")
        sys.exit(1)


    print("YO")
    with open("/home/baston/boo", "w") as boo:
        boo.write("hello")


