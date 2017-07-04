
import sys
import os
import re

class cfile:


    def __init__(self, file_path):
        self.file_path = file_path
        f = open(file_path) 
        self.list_of_lines = f.readlines()

    def first_pass(self):
        i = 0
        for line in self.list_of_lines:
            if(re.match(r"\w*\/*#")):
                #find matching end
                j = i+1
                for line in self.list_of_lines[i:]:
                    if(re.match(r"\w*\*\/")):
                        a=2
                    j = j+1
                i=i+1
            

def test():
    cf = cfile("test_A.c")
    print(cf.str)

    print("cfile.py self-test passed")
    return True


if __name__ == "__main__":
    assert(test())