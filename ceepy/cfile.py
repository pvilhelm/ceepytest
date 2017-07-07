

import sys
import os
import re
from io import StringIO

from asserts import *

VALID_COMP_LIST = ["==","!=","<",">","!>","!<","<=",">="]

class cfile:
    def __init__(self, file_path):
        self.file_path = file_path
        f = open(file_path,'r',encoding='utf-8-sig')
        self.full_str = f.read()

        self.file_name = os.path.basename(file_path)

        self.dict_local_vars = {"C":"//", "C0":"/*", "C1":"*/"}
        exec("from eval_util import *",{},self.dict_local_vars)
        self.dict_global_vars = {}
        self.dict_assigns = {}
        self.dict_asserts = {}
        self.dict_fcn_decls = {}

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
        #find all patterns /*# ... #*/ 
        for m in re.finditer(r"\/\*#(.*?)(#\*\/)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = m[1].strip()
            self.dict_strs[m.start(1)] = {"type":"py_inline","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}
            if(m[0].find('\n')!=-1):    #code segment spans multiple lines so add new line to the output later
                self.dict_strs[m.start(1)]["inline"] = False
            else:
                self.dict_strs[m.start(1)]["inline"] = True

        #find all patterns //# ... \n
        for m in re.finditer(r"\/\/#(.*?)(\n)",self.full_str, re.DOTALL | re.MULTILINE):
            tmp_str = "\n"+m[1].strip() 
            self.dict_strs[m.start(1)] = {"inline":False,"type":"py_inline","start":m.start(1),"end":m.end(1),"after":m.end(2),"str":tmp_str}

        

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
                self.c_str_additions[d["after"]] = (" " if d["inline"] else "\n") + self.py_inline(d["str"])

        #add the python inline code output to the c-file
        self.out_c_str = ""

        pos_to_add_to = sorted(self.c_str_additions.keys())
        
        #stich the strings together
        old_pos = 0
        for pos in pos_to_add_to:
            self.out_c_str += self.full_str[old_pos:pos] 
            self.out_c_str += self.c_str_additions[pos] 
            old_pos = pos 
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
        self.l_test_fcn_names = ["ceepytest_"+self.file_name.replace(".","_DOT_").replace(" ","_SPACE_")]
        self.out_c_str +="\n\nint "+self.l_test_fcn_names[0]+"(){\n"
        for pos in pos_to_add_to:
            for line in self.c_str_additions[pos].splitlines():
                self.out_c_str += "    " + line + "\n"
        self.out_c_str += "    return 0;\n"
        self.out_c_str += "}\n"
        self.c_str_additions.clear() 

    def remove_ceepyt_comment_lines(self,str):
        str_ret = ""
  
        ls = []
        for line in str.splitlines():
            r = re.fullmatch(r'^((?:(?:[^\\\n])|(?:\\.))*?)§(.*)$',line)
            # matches --> qweqwe \§  § qweqwewqe
            # or  -->  § qeqweqwe §§§§§
            # etc, but not: qwe("\§");
            if r:
                if r[1].isspace() or len(r[1]) == 0: #only white space before comment
                    continue # is a comment §
                else:#otherwise append non-comments to list
                    ls.append(r[1].replace(r"\§","§")) #replaces escaped §:s 
            else:#no comments in line
                ls.append(line)
        
        #preserve ending new line in str    
        if(str[-1]=="\n"):#original string ended with \n
            return "\n".join(ls)+"\n"
        else:
            return "\n".join(ls)

         

    def py_inline(self, str):
        str = self.remove_ceepyt_comment_lines(str)
        old_stdout = sys.stdout
        my_stdout = sys.stdout = StringIO()
        exec(str,self.dict_global_vars,self.dict_local_vars)
        sys.stdout = old_stdout
        ret_str = my_stdout.getvalue()
        my_stdout.close()
        return ret_str

    def assigns(self, str):
        str = self.remove_ceepyt_comment_lines(str)

        #setup enviroment
        dir_locals = {}
        exec("from eval_util import *",{},dir_locals)

        #iterate over the assigns expressions and evaluate the right hand side
        #and assign its value to the left hand side and add it to assign dict
        for a in re.finditer(r"^\s*(\w+[\w\d]*)\s*=\s*(.+)\s*$",str,re.MULTILINE):
            name = a[1]
            value = a[2]
            self.dict_assigns[name] = eval(value,{},dir_locals)
        
        #iterate over assigns and find function "redeclarations" e.g.  " volatile int* add() "
                            #reg ex or line noise? Sorry ... it finds "type name(w/e);"
        for a in re.finditer(r"^\s*((?:(?:[\w*]+?[\w\d*]*?)+?\s*)+?)(\w+[\w\d]*\(\s*\))\s*;?\s*$",str,re.MULTILINE):
            type = a[1]
            name = a[2]
            self.dict_fcn_decls[name] = type
        return ""

    def asserts(self,str):
        str = self.remove_ceepyt_comment_lines(str)

        str_ret = ""
        #iterate over the assert lines and find lh, comparasion and rh
        for a in re.finditer(r'^\s*(.*?)\s*([=!<>]{1,2})\s*(#)?(.+?)\s*$',str,re.MULTILINE):

            #check if lh is a "redeclared" function
            lh = a[1]
            r =  re.match(r'^\s*(\w+[\w\d]*)\s*\(.*\)\s*$',lh)
            if(r): #its a function on lh
                f_type = self.dict_fcn_decls.get(r[1]+"()") 
                if not f_type: # no type specified in the code
                    f_type = "verbatim"
            else:
                f_type = "verbatim"


            comp = a[2]
            if(a[3]):#if theres a # infront of rh expression it's python code
                rh = eval(a[4],{},{}).__str__() #eval python code
            else:
                rh = a[4]


                # ok so add this if thers gonna be problem with comparing floats and doubles
            #if lh is float, convert rh string so it ends with f
            #if f_type.find("float")>0:
                #check if rh is not a floating point literal
                #iterate over all float literals and add f if missing (so that printf doesnt
                # try 
            #    for r in re.finditer(r'\s*[+-]?\s*\d*\.?\d*(?:(?:e|E)[+-]?\d*)?([fFLl])?\s*',rh):
                 

            if comp not in VALID_COMP_LIST:
                raise RuntimeError(comp+"not in VALID_COMP_LIST")
            if comp == "==":
                str_ret += assert_eq(lh,rh,f_type)
            elif comp == "!=":
                str_ret += assert_not_eq(lh,rh,f_type)
            elif comp == "<=":
                str_ret += assert_less_eq(lh,rh,f_type)
            elif comp == ">=":
                str_ret += assert_greater_eq(lh,rh,f_type)
            elif comp == ">":
                str_ret += assert_greater(lh,rh,f_type)
            elif comp == "<":
                str_ret += assert_less(lh,rh,f_type)
            elif comp == "!<":
                str_ret += assert_greater_eq(lh,rh,f_type)
            elif comp == "!>":
                str_ret += assert_less_eq(lh,rh,f_type)
            else:
                raise RuntimeError(comp+"is missed in switch case statements")

        return str_ret

    def save(self,path):
        f = open(path,'w', encoding='utf-8-sig')
        f.write(self.out_c_str)

def test():
    cf = cfile("test_A.ct")
    cf.save("out.c")
    print("cfile.py self-test might have passed (it didn't raise errors, so check output file manually)")
    return True


if __name__ == "__main__":
    assert(test())