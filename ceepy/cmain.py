
import cfile
import datetime
import os

class cmain:

    def __init__(self):
        self.l_cfiles = []

    def add_cfile(self, cf):
        self.l_cfiles.append(cf)

    def make_test_files(self, trgt_folder, trgt_test_c,ceepy_path): 
        self.ceepy_path = ceepy_path #path to ceepy module
        self.trgt_folder = trgt_folder #folder to put generated files in
        self.name = trgt_test_c #name of test
        
        #save .ct-files to target folder
        for cf in self.l_cfiles:
            cf.save(self.trgt_folder+"/"+cf.file_name.replace(".ct",".c"))
        
        #make main file and save it in target folder
        str_main = self.make_main_file(self.trgt_folder)
        f = open(self.trgt_folder+"/"+self.name+".c",'w', encoding='utf-8-sig')
        f.write(str_main)
         
        #make compile bat file
        str_comp_script = self.make_compile_script()
        f = open(self.trgt_folder+"/compile_"+self.name+".bat",'w', encoding='utf-8-sig')
        f.write(str_comp_script)
        f.close()

    def make_main_file(self, path):
        str_main = ""
        str_main += " /* A test generated with Ceepytest timestamp: "+datetime.datetime.now().__str__()+" */\n"+"\n"
        str_main += "#include <stdio.h>\n"
        str_main += "#include <stdlib.h>\n"+"\n"
        str_main += '#include "asserts.h"\n'+"\n"

        #generate external links to test functions 
        for cf in self.l_cfiles:
            str_main += "/* External test functions from file "+cf.file_name+" */\n"
            for fcn in cf.l_test_fcn_names:
                str_main += "extern int "+fcn+"();\n"
            str_main +="\n"

        #generate main function
        str_main += "int main(int argc, char** argv){\n"
        str_main += "\n"
        str_main += "    "+'printf("Staring test!\\n\\n");\n'
        str_main += "\n"
        str_main += "    "+"/* Iterate all registred tests ... */\n"
        str_main += "\n"

        
        #generate function calls and checks for all tests 
        for cf in self.l_cfiles:
            str_main += "    "+"/* Test functions from file "+cf.file_name+" */\n"
            str_main += "    "+'printf("Starting sub-tests in: '+cf.file_name+'\\n");\n'
            for fcn in cf.l_test_fcn_names:
                str_main += "    "+"    "+'printf("\\n    Starting sub-test '+fcn+'() ... \\n\\n");\n'
                str_main += "    "+"if("+fcn+"()){\n"
                str_main += "    "+"    "+"/* Test failed */\n"
                str_main += "    "+"    "+'printf("Test '+fcn+'() failed\\nAborting ...\\n");\n'
                str_main += "    "+"    "+'exit(EXIT_FAILURE);\n'
                str_main += "    "+"} else {\n"
                str_main += "    "+"    "+"/* Test suceeded */\n"
                str_main += "    "+"    "+'printf("\\n    Sub-test '+fcn+'() passed ... \\n\\n");\n'
                str_main += "    "+"}\n"
            str_main +="\n"
            str_main += "    "+'printf("Sub-tests passed in: '+cf.file_name+'\\n\\n");\n'
        str_main += "\n"

        #end test
        str_main += "    "+"/* All tests passed */\n"
        str_main += "    "+'printf("\\nAll tests passed!\\n");\n'
        str_main += "    "+"return EXIT_SUCCESS;\n"
        str_main += "}\n"

        return str_main

    def make_compile_script(self):

        ret_str = ""
        ret_str += "cd /D "+os.path.abspath(self.trgt_folder)+"\n"
        ret_str += "cl -TC * "+self.ceepy_path+"\\src\\asserts.c"+" "+"-I"+" "+self.ceepy_path+"\\includes"+"\n"

        return ret_str