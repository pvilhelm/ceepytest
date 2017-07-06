import os
import subprocess
import pathlib
import re

import cfile
import cmain

def main():
    #ans = subprocess.run("echo hej",shell=True,stdout=subprocess.PIPE)
    curr_dir = os.getcwd()

    trgt_folder = "ceepy_test"
    trgt_test_c = "test_main.c"

    try:
        os.mkdir(trgt_folder)
    except:
        print("Directory "+trgt_folder+" allready exists")

    pathlist = pathlib.Path(".").glob('*.ct')
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
    main()

