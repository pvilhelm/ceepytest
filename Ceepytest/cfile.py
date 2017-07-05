

import sys
import os
import re
from io import StringIO

from asserts import *

VALID_COMP_LIST = ["==","!=","<",">","!>","!<","<=",">="]

class cfile:

    def __init__(self, file_path):
        self.file_path = file_path
        f = open(file_path)
        self.full_str = f.read()

        self.file_name = os.path.basename(file_path)
        self.dict_local_vars = {"C":"//", "C0":"/*", "C1":"*/"}
        self.dict_global_vars = {}
        self.dict_assigns = {}
        self.dict_asserts = {}

        # Parse Ceepytest code snipps
        self.first_pass()
        # Evaluate all those snipps
        self.sec_pass()
        #
        self.third_pass()
        

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
        
        self.c_str_additions.clear()

        #if(old_pos<len(self.out_c_str)): #uneccesary?
        self.out_c_str += self.full_str[old_pos:]
        
        # Assignments
        #find all patterns /*! ... */
        for m in re.finditer(r"\/\*!(.*?)(!\*\/)",self.out_c_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"assigns","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}
        #find all patterns //!
        for m in re.finditer(r"\/\/!(.*?)(\n)",self.out_c_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"assigns","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}

        # Asserts
        #find all patterns /*? ... */
        for m in re.finditer(r"\/\*\?(.*?)(\?\*\/)",self.out_c_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"asserts","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}
        #find all patterns //?
        for m in re.finditer(r"\/\/\?(.*?)(\n)",self.out_c_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"asserts","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}
        #for k,v in self.dict_strs.items():
        #    print("key:"+str(k))
        #    for k,v in v.items():
        #        print("\t"+str(k)+":"+str(v))

        #process assigns
        for k in sorted(self.dict_strs.keys()):
            d = self.dict_strs[k]
            if d["type"]=="assigns":
                self.assigns(d["str"])

    def third_pass(self):
        #process asserts
        for k in sorted(self.dict_strs.keys()):
            d = self.dict_strs[k]
            if d["type"]=="asserts":
                self.c_str_additions[d["after"]] = self.asserts(d["str"])

        #add the python inline code output to the c-file
        #out_c_str_old = self.out_c_str #copy from out string
        #self.out_c_str = "" #reset it first

        pos_to_add_to = sorted(self.c_str_additions.keys())
        
        #stich the strings together
        old_pos = 0
        self.out_c_str +="\n\nint ceepytest_"+self.file_name.replace(".","_DOT_").replace(" ","_SPACE_")+"(){\n"
        for pos in pos_to_add_to:
            self.out_c_str += "    "+self.c_str_additions[pos]
        self.out_c_str += "}\n"
        self.c_str_additions.clear() 


    def py_inline(self, str):    
        old_stdout = sys.stdout
        my_stdout = sys.stdout = StringIO()
        exec(str,self.dict_global_vars,self.dict_local_vars)
        sys.stdout = old_stdout
        ret_str = my_stdout.getvalue()
        my_stdout.close()
        return ret_str

    def assigns(self, str):
        #setup enviroment
        dir_locals = {}
        exec("from math import *",{},dir_locals)

        #iterate over the assigns expressions and evaluate the right hand side
        #and assign its value to the left hand side and add it to assign dict
        for a in re.finditer(r"^\s*(\w+[\w\d]*)\s*=\s*(.+)\s*$",str,re.MULTILINE):
            name = a[1]
            value = a[2]
            self.dict_assigns[name] = eval(value,{},dir_locals)
        return ""

    def asserts(self,str):

        str_ret = ""
        #iterate over the assert lines and find lh, comparasion and rh
        for a in re.finditer(r'^\s*([\w"]+(?:(?:->)|[\w\d.()"])*)\s*([=!<>]{1,2})\s*("?[\w\d.]+"?)\s*$',str,re.MULTILINE):
            lh = a[1]
            comp = a[2]
            rh = a[3]
            if comp not in VALID_COMP_LIST:
                raise RuntimeError(comp+"not in VALID_COMP_LIST")
            if comp == "==":
                str_ret += assert_eq(lh,rh)
            elif comp == "!=":
                str_ret += assert_not_eq(lh,rh)
            elif comp == "<=":
                str_ret += assert_less_eq(lh,rh)
            elif comp == ">=":
                str_ret += assert_greater_eq(lh,rh)
            elif comp == ">":
                str_ret += assert_greater(lh,rh)
            elif comp == "<":
                str_ret += assert_less(lh,rh)
            elif comp == "!<":
                str_ret += assert_greater_eq(lh,rh)
            elif comp == "!>":
                str_ret += assert_less_eq(lh,rh)
            else:
                raise RuntimeError(comp+"is missed in switch case statements")

        return str_ret

def test():
    cf = cfile("test_A.c")
    print(cf.out_c_str)
    print("cfile.py self-test passed")
    f = open("out.c",'w')
    f.write(cf.out_c_str)
    return True


if __name__ == "__main__":
    assert(test())