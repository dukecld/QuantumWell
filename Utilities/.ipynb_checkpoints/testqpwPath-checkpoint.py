import pathlib
import sys
import os
from pathlib import Path

# qpw directory name
qpwDir = 'PotentialWell'

# current working directory
cwdP = Path.cwd()
qpwPath = Path()
print('cwd ',cwdP)
print('qpwDir',qpwDir)

# home directory
homeP = Path.home()
print('homeP ',homeP)

# tests
if cwdP.parent.name == qpwDir:
    qpwPath = cwdP.parent
elif cwdP.name == qpwDir:
    qpwPath = cwdP
elif (cwdP / qpwDir).is_dir():
    qpwPath = (cwdP / qpwDir)


print(qpwPath)
