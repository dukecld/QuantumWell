import sys
import os
from pathlib import Path

def setPath(pathToAdd = ""):
    """ add PotentialWell/src path to sys.path, use with python >= 3.4

    Enables use of PotentialWell/src modules in scripts from
    any directory without copying these modules to that
    directory.

    pathToAdd == "": current directory is a PotentialWell directory or
                     parent directory is a PotentialWell directory

    e.g. you are creating scripts in the PotentialWell/Notebooks directory
    and wish to use modules in the PotentialWell/src directory.

    Usage:  Copy setPath.py to your current directory and include
            these lines in your script:

                from setPath import setPath
                setPath()  # if you are in a child directory
                           # or a PotentialWell directory

                # or give a specific path to a PotentialWell directory
                setPath('<path to PotentialWell directory>')

                print(sys.path) # if you want to confirm the path addition
    """

    # get name of parent directory, add '/src', add to system path
    # can now import modules from src directory

    path = Path.cwd()
    patha = Path()
    if pathToAdd != "":
        path = Path(pathToAdd)

    # is path a PotentialWell directory

    if path.name == 'PotentialWell':
        print('cwd is a PotentialWell directory')
        patha = path
    elif str(path.parent.name) == 'PotentialWell':
        #print('parentDir is a PotentialWell directory')
        patha = path.parent
    else:
        print('neither specified directory nor the parent')
        print('directory is a PotentialWell directory')
        print('     returning with no path addition')
        return

    #print('success ',path)
    newPath = str(patha.joinpath('src'))
    sys.path = [newPath] + sys.path
    print('adding to sys.path ',str(newPath))

    return

# ===================================================
if __name__ == "__main__":
    print('Testing setPath with __main__')
    print('before ',sys.path)
    setPth = setPath()
    print('\nafter ',sys.path)
