
import sys
import os
import re
from io import StringIO

class cfile:


    def __init__(self, file_path):
        self.file_path = file_path
        f = open(file_path) 
        self.full_str = f.read()

        self.dict_local_vars = {"C":"//", "C0":"/*", "C1":"*/"}
        self.dict_global_vars = {}
        # Parse Ceepytest code snipps
        self.first_pass()
        # Evaluate all those snipps
        self.sec_pass()
        

    def first_pass(self):
        """Parse a c-file for Ceepytest patterns and store the corrensponding strings."""

        self.dict_strs = {} #dict of dict of dict of segment of text
        #first dict: key
        
        # Python inline code
        #find all patterns /*# ... */ 
        for m in re.finditer(r"\/\*#(.*?)(#\*\/)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"py_inline","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}
            if(m[0].find('\n')!=-1):    #code segment spans multiple lines so add new line to the output later
                self.dict_strs[m.start(1)]["inline"] = True
            else:
                self.dict_strs[m.start(1)]["inline"] = False

        #find all patterns //# ... \n
        for m in re.finditer(r"\/\/#(.*?)(\n)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = "\n"+m[1].strip() 
            self.dict_strs[m.start(1)] = {"type":"py_inline","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}

        

    def sec_pass(self):
        """Construct c-code for inline python """
        
        self.c_str_additions = {}

        #iterate over all dict entrys and call the correct function if the entry
        #needs to be run before other code (i.e inline python code that can write
        #more Ceepytest code) /*# ... #*/
        for k in sorted(self.dict_strs.keys()):
            d = self.dict_strs[k]
            type = d["type"]
            if(type == "py_inline"):
                self.c_str_additions[d["after"]] = ("\n" if d["inline"] else " ") + self.py_inline(d["str"])

        #add the python inline code output to the c-file
        self.out_c_str = ""

        pos_to_add_to = sorted(self.c_str_additions.keys())
        
        #stich the strings together
        old_pos = 0
        for pos in pos_to_add_to:
            self.out_c_str += self.full_str[old_pos:pos]
            #self.out_c_str += "/* Start generated code from pos: %s */\n" % pos
            self.out_c_str += self.c_str_additions[pos]
            #self.out_c_str += "/* End generated code from pos: %s */\n" % pos
            old_pos = pos
            print(self.full_str+"\n")
        
        #if(old_pos<len(self.out_c_str)): #uneccesary?
        self.out_c_str += self.full_str[old_pos:]
        
        # Assignments
        #find all patterns /*! ... */
        for m in re.finditer(r"\/\*!(.*?)(!\*\/)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"assigns","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}
        #find all patterns //!
        for m in re.finditer(r"\/\/!(.*?)(\n)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"assigns","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}

        # Asserts
        #find all patterns /*? ... */
        for m in re.finditer(r"\/\*\?(.*?)(\?\*\/)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"asserts","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}
        #find all patterns //?
        for m in re.finditer(r"\/\/\?(.*?)(\n)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"asserts","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}
        #for k,v in self.dict_strs.items():
        #    print("key:"+str(k))
        #    for k,v in v.items():
        #        print("\t"+str(k)+":"+str(v))

    def third_pass(self):
        NOP

    def py_inline(self, str):    
        old_stdout = sys.stdout
        my_stdout = sys.stdout = StringIO()
        exec(str,self.dict_global_vars,self.dict_local_vars)
        sys.stdout = old_stdout
        ret_str = my_stdout.getvalue()
        my_stdout.close()
        return ret_str

    def assigns(self, str):
        ret_str = ""
        self.dict_assigns = {}



        return ret_str

def test():
    cf = cfile("test_A.c")
    print(cf.out_c_str)
    print("cfile.py self-test passed")
    return True


if __name__ == "__main__":
    assert(test())