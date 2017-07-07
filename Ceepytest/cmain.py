
import cfile
import datetime

class cmain:

    def __init__(self):
        self.l_cfiles = []

    def add_cfile(self, cf):
        self.l_cfiles.append(cf)

    def make_test_files(self, path, name):

        for cf in self.l_cfiles:
            cf.save(path+"/"+cf.file_name.replace(".ct",".c"))
        
        str_main = self.make_main_file(path)
        f = open(path+"/"+name,'w', encoding='utf-8')
        f.write(str_main)

        #cl -TC test_A.c test_main.c ./../asserts.c -I ./..

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
            for fcn in cf.l_test_fcn_names:
                str_main += "    "+"if("+fcn+"()){\n"
                str_main += "    "+"    "+"/* Test failed */\n"
                str_main += "    "+"    "+'printf("Test '+fcn+'() failed\\nAborting ...\\n");\n'
                str_main += "    "+"    "+'exit(EXIT_FAILURE);\n'
                str_main += "    "+"} else {\n"
                str_main += "    "+"    "+"/* Test suceeded */\n"
                str_main += "    "+"    "+'printf("Test '+fcn+'() passed ... \\n");\n'
                str_main += "    "+"}\n"
            str_main +="\n"
        str_main += "\n"

        #end test
        str_main += "    "+"/* All tests passed */\n"
        str_main += "    "+'printf("\\nAll tests passed!\\n");\n'
        str_main += "    "+"return EXIT_SUCCESS;\n"
        str_main += "}\n"

        return str_main