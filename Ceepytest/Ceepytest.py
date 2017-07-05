import os
import subprocess
import pathlib

def main():
    ans = subprocess.run("echo hej",shell=True,stdout=subprocess.PIPE)
    curr_dir = os.getcwd()

    pathlist = pathlib.Path(".").glob('*.c')
    for i in pathlist:
        print(i)

if __name__ == "__main__":
    main()

