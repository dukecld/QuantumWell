import sys
import pathlib
from pathlib import Path

def setPath(path=sys.path,filename='config',varname='path',subdir='src'):
    """appends to sys path from config file in ~/qwConfig directory

    path: 
    """
    
    configP = Path.home() / 'qwConfig' / 'config'

    with open(configP, mode='r') as fid:
        pathL = [line.strip() for line in fid if
        line.startswith('path')]
    if len(pathL) != 1:
        print('no path value found in config file')
        print('no addition to sys.path , returning')
        return None
    
    pathS = str(pathL[0])
    tmp,pathQ = pathS.split('=')
    pathQ = pathQ.strip()

    return pathQ


