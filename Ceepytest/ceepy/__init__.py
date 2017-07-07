import os
import sys
import subprocess
import pathlib
import re

import cfile
import cmain

help = """ Ceepy Test is a C testing framework.

Usage:
    -h : Prints this text

"""

def main(argv):

    trgt_folder = "ceepy_test"
    trgt_test_c = "test_main.c"
    src_folder = "."
    for i in range(0,len(argv)):
        if i == 0:
            continue
        s = argv[i]

        if re.fullmatch(r'-h',s):
            print(help)
            sys.exit(0)
        elif re.fullmatch(r'-t',s):
            if i+1 >= len(argv):
                print(help)
                sys.exit("Syntax error!")
            trgt_folder = argv[i+1]
        elif re.fullmatch(r'-s',s):
            if i+1 >= len(argv):
                print(help)
                sys.exit("Syntax error!")
            src_folder = argv[i+1]


    #ans = subprocess.run("echo hej",shell=True,stdout=subprocess.PIPE)
    curr_dir = os.getcwd()

    

    try:
        os.mkdir(trgt_folder)
    except:
        print("Directory "+trgt_folder+" allready exists")

    pathlist = pathlib.Path(src_folder).glob('*.ct')
    l_test_files = []
    for i in pathlist:
        l_test_files.append(cfile.cfile(i))

    for f in l_test_files:
        f.save(trgt_folder+"/ct_"+re.sub(r'\.[^.]*$',"",f.file_name)[1]+".c")

    #make main c file 
    cm = cmain.cmain()
    for f in l_test_files:
        cm.add_cfile(f)

    cm.make_test_files(trgt_folder,trgt_test_c)
    
    #compile the test


if __name__ == "__main__":
    argv = sys.argv
    
    if(len(argv)==0):
        argv = [os.getcwd()] 

    main(argv)

