
import sys
import os

class cfile:


    def __init__(self, file_path):
        self.file_path = file_path
        f = open(file_path) 
        self.str = f.readlines()

def test():
    cf = cfile("test_A.c")


if __name__ == "__main__":
    test()
