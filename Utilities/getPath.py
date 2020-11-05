""" getPath from config file in $HOME/qwConfig
working version
"""
import sys
import pathlib
from pathlib import Path

def getPath(filename='config',parmName='path',subdir='src'):
    """get path to QuantumWell and to subdirectory from designated
       file in $home/qwConfig directory

    Parameters:
        filename (default 'config'): name of config file in qwConfig directory
        parmName (default 'path'): parameter name in config file
        subdir (default 'src'): name of 'path' subdirectory

    Returns: tuple of two strings (qPath,qPathSubDir)
        qPath: path to QuantumWell directory
        qPathSubDir: path to subdirectory of QuantumWell directory
        
        if subdir is None or subdir == ''
        returns (qPath,qPath)

    Usage: In python code or jupyter notebook to add path to
           QuantumWell directory:
        import sys
        from getPath import getPath

        pathTuple = getPath()
        sys.path = sys.path.insert(0,pathTuple[0])
        print(sys.Path)
        
        or use the setPath function that is also in getPath.py
    """
    confDir = 'qwConfig'
    configP = Path.home() / confDir / filename
    if configP.is_file():
        with open(configP, mode='r') as fid:
            pathL = [line.strip() for line in fid if
            line.startswith(parmName)]
        if len(pathL) != 1:
            print('no ',parmName,' line found in ',str(configP))
            print('returning None')
            return None
    else:
        print('cannot find: ',str(configP))
        print('returning None')
        return None

    pathS = str(pathL[0])
    tmp,pathQ = pathS.split('=')
    pathQ = pathQ.strip()
    path1 = Path(pathQ)
    if subdir is None or subdir == '':
        path2 = path1
    else:
        path2 = path1 / subdir
    if not path2.is_dir():
        print('directory ',str(path2),' does not exist')
        #print('adding path to path1',str(path1))
        #path2 = path1
        print('returning None')
        return None
    pathAll = (str(path1),str(path2))

    return pathAll

# ==========================================================

def setPath(sysP,subdr = 'src'):
    """ adds path to QuantumWell/src to sys.path
    
    Parameters:
        sysP: sys.path list from calling program
        subdir (default='src'): subdirectory of QuantumWell directory
    
    Returns: True if add path was successful
    """
    returnB = True
    
    # get the new path from getPart function
    pathToDir = getPath(subdir = subdr)
    
    if pathToDir == '' or pathToDir is None:
        returnB = False
    else:
        # insert the new path at the beginning of sys.path list
        sysP.insert(0,pathToDir[1])

    return returnB
    
# this section executes with 'python getPath.py' and serves as example usage in python scripts
if __name__=="__main__":
    # test getPath when True
    print('starting main')
    if False:
        print('\ngetPath example')

        path12 = getPath(subdir='src')
        if path12:
            print('\nfound tuple')
            print(path12)
            print('\ninserting ',path12[1],' at start of sys.path list')
            sys.path.insert(0,path12[1])
            print('\nprinting sys.path')
            print(sys.path)
            print('\n')
        else:
            print('findPath returned None')
            
    # test setPath if True
    if True:
        print('old sys.path')
        print(sys.path)
        print('\n')
        newsrc = setPath(sys.path,subdr = 'src')
        print('new sys.path')
        print(sys.path)
        