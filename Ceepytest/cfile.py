
import sys
import os
import re
from io import StringIO

class cfile:


    def __init__(self, file_path):
        self.file_path = file_path
        f = open(file_path) 
        self.full_str = f.read()

        # Parse Ceepytest code snipps
        self.first_pass()
        # Evaluate all those snipps
        self.sec_pass()

    def first_pass(self):
        """Parse a c-file for Ceepytest patterns and store the corrensponding strings."""

        self.list_of_lines = []
        self.list_of_py_str_span_tuples = []
        self.list_of_assign_str_span_tuples = []
        self.list_of_assert_str_span_tuples = []
        self.dict_strs = {} #dict of dict of dict of segment of text
        #first dict: key
        
        # Python inline code
        #find all patterns /*# ... */ 
        for m in re.finditer(r"\/\*#(.*?)(\*\/)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip() 
            self.dict_strs[m.start(1)] = {"type":"py_inline","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}
        #find all patterns //# ... \n
        for m in re.finditer(r"\/\/#(.*?)(\n)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"py_inline","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}

        # Assignments
        #find all patterns /*! ... */
        for m in re.finditer(r"\/\*!(.*?)(\*\/)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"assigns","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}
        #find all patterns //!
        for m in re.finditer(r"\/\/!(.*?)(\n)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"assigns","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}

        # Asserts
        #find all patterns /*? ... */
        for m in re.finditer(r"\/\*\?(.*?)(\*\/)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"asserts","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}
        #find all patterns //?
        for m in re.finditer(r"\/\/\?(.*?)(\n)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"asserts","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}
        for k,v in self.dict_strs.items():
            print("key:"+str(k))
            for k,v in v.items():
                print("\t"+str(k)+":"+str(v))

    def sec_pass(self):
        """ Construct c-code for all Ceepytest strings found in the file"""

        #iterate over all dict entrys and call the correct function
        for k in sorted(self.dict_strs.keys()):
            d = self.dict_strs[k]
            type = d["type"]
            if(type == "py_inline"):
                py_inline(d["str"])

    def py_inline(self, str):    
        old_stdout = sys.stdout
        my_stdout = sys.stdout = StringIO()
        eval()
        sys.stdout = self.old_stdout

        print(my_stdout.getvalue())
        my_stdout.close()


def test():
    cf = cfile("test_A.c")
    cf.first_pass()

    print("cfile.py self-test passed")
    return True


if __name__ == "__main__":
    assert(test())