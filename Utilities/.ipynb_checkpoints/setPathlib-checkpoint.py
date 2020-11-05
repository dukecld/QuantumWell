import sys
import os
from pathlib import Path

def setPathlib(pathToAdd = ""):
    """ add PotentialWell/src path to sys.path 
        
    Enables use of PotentialWell/src modules in scripts in 
    any directory without copying these modules to the 
    current directory. 
    
    if pathToAdd == "", assumes current working directory 
    is child directory of PotentialWell directory, e.g. you  
    are creating scripts in the PotentialWell/Notebooks directory.

    Usage:  Copy setPath.py to your current directory and include
            in yout script:
    
                from setPath import setPath
                setPath()  #if you are in a child directory
                or
                setPath('<path to PotentialWell directory>')
    """

    # get name of parent directory, add '/src', add to system path
    # can now import modules from src directory

    pathB = True
    
    if pathToAdd == "":
        #parent = os.path.dirname(os.getcwd())
        path = Path.cwd()
    else:
        path = Path(pathToAdd)

    print('path',path)
    
    # is path a PotentialWell directory
    
    if path.name == 'PotentialWell':
        print('cwd is a PotentialWell directory')
        
    elif str(path.parent.name) == 'PotentialWell':
        print('parentDir is a PotentialWell directory')
        path = path.parent
    else:
        print('neither specified directory nor the parent')
        print('  directory is a PotentialWell directory')
        print('     returning with no path addition')
        return
    
    print('success ',path)
    newPath = str(path.joinpath('src'))
    sys.path = [newPath] + sys.path
    print('adding to path ',str(newPath))


    return

    if True:
        # see if directory is PotentialWell directory
        path_sep = os.path.sep
        parentlist = parent.split(path_sep)
        lastDir = parentlist[len(parentlist) - 1]
        #print('lastDir',lastDir)
        if lastDir != 'PotentialWell':
            print(parent," directory is not PotentialWell directory")
            print('move notebook to a child directory of PotentialWell or')
            print('enter the correct path to your PotentialWell directory')
            print('in setPath')

        else:
            newPath = os.path.join(parent,'src')
            sys.path = [newPath] + sys.path
            print('adding to path ',newPath)
