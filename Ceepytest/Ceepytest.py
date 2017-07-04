
import os
import subprocess




def main():
    ans = subprocess.run("echo hej",shell=True,stdout=subprocess.PIPE)

if __name__ == "__main__":
    main()

