""" findPath from config file in $HOME/qwConfig
"""
import sys
import pathlib
from pathlib import Path

def findPath(filename='config',parmName='path',subdir='src'):
    """find path to QuantumWell from designated file in $home/qwConfig directory

    Execute this file to run example code at the end of this file "python findPath.py"

    Parameters:
        filename (default 'config'): name of file in qwConfig directory
        parmName (default 'path'): parameter name in file
        subdir (default 'src'): subdirectory of path subdirectory

    Returns: tuple of two strings (qPath,qPathSubDir)
        qPath: path to QuantumWell subdirectoryh
        qPathSubDir: path to subdirectory of QuantumWell directoryyt

    Usage: In python code or jupyter notebook to add path to QuantumWell directory:
        import sys
        from findPath import findPath

        pathTuple = findPath()
        sys.path = sys.path.insert(0,pathTuple[0])
        print(sys.Path)
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
    path2 = path1 / subdir
    if not path2.is_dir():
        print('directory ',str(path2),' does not exist')
        print('returning None')
        return None
    pathAll = (str(path1),str(path2))

    return pathAll

# ==========================================================
# this section executes with 'python findPath.py' and serves as example usage in python scripts
if __name__=="__main__":
    print('findPath example')

    path12 = findPath(subdir='src')
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
