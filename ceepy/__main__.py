import os
import sys
import subprocess
import pathlib
import re
import argparse

import cfile
import cmain

""" Ceepy Test is a C testing framework.

Usage:
    -h : Prints this text

"""

def main(argv):
    parser = argparse.ArgumentParser(prog = "ceepy")
    parser.add_argument("-f","--src_files",nargs="*",default = [], help="Source test files (replaces -s folder i specified).") 
    parser.add_argument("-t","--trgt_dir", nargs="?", default = "ceepy_test", help="Target folder to generate the test into.")
    parser.add_argument("-s","--src_dir", nargs="?", default = ".", help="Source folder to scan for *.ct files to generate test off.")
    parser.add_argument("-n", "--test_name", nargs="?", default = "test", help="Name of the generated test.")

    if "-h" in argv[1:]:
        print("""\nCeepy Test - a pytonic PHP/JSP wanna-be C Test Frame Work!

        (c) Petter Tomner, no rights reserved.
        Contact: petter.vilhelm@gmail.com\n\n""")

    p = parser.parse_args(argv[1:])

    trgt_folder = p.trgt_dir
    trgt_test_c = p.test_name
    src_folder = p.src_dir
    pathlist = p.src_files

    ceepy_file_path = os.path.realpath(__file__)
    ceepy_path = os.path.dirname(ceepy_file_path)
    curr_dir = os.getcwd()

    #ans = subprocess.run("echo hej",shell=True,stdout=subprocess.PIPE)
    

    

    try:
        os.mkdir(trgt_folder)
    except:
        print("Directory "+trgt_folder+" allready exists")

    #if no soruce files have been specified, process all .ct files in the provided source folder (default ".")
    if not pathlist:
        pathlist = pathlib.Path(src_folder).glob('*.ct')

    l_test_files = []
    for i in pathlist:
        if pathlib.Path(i).stem == trgt_test_c:
            print("Test file "+i+" will have same name as the main C-file "+trgt_test_c+".c\n")
            print(__doc__)
            sys.exit(-1)
        l_test_files.append(cfile.cfile(i))

    #for f in l_test_files:
    #    f.save(trgt_folder+"/ct_"+re.sub(r'\.[^.]*$',"",f.file_name)[1]+".c")

    #make main c file 
    cm = cmain.cmain()
    for f in l_test_files:
        cm.add_cfile(f)

    cm.make_test_files(trgt_folder,trgt_test_c,ceepy_path)
    
    #compile the test


if __name__ == "__main__":
    argv = sys.argv
    

    if(len(argv)==0):
        argv = [os.getcwd()] 

    main(argv)

