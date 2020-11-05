""" moduleAndPythonCheck modules, includes test for module and obtain Python version

    testExistence(module)
    getPythonVersion()
"""
import importlib
import sys

def existModule(module):
    """ function to determine if a module or package exists
    Parameter: module - string, e.g. matplotlib
    Returns: True if found, False if not found
    """

    #testExist = importlib.util.find_spec(module)
    testExist = importlib.find_loader(module)
    found = testExist is not None
    return found

def getPythonVersion():
    """ function to obtain current Python version
    Returns: tuple of integers (major version, minor version)
             e.g (3,8) for version 3.8
    """
    vers_major = sys.version_info.major
    vers_minor = sys.version_info.minor
    vers = str(vers_major) + '.' + str(vers_minor)

    return (vers_major,vers_minor)

if __name__ == "__main__":
    print('\nChecking python version, must be 3.6 or greater')
    versT = getPythonVersion()
    vers_major = versT[0]
    vers_minor = versT[1]
    vers = str(vers_major) + '.' + str(vers_minor)

    print('     you are using python version ',vers)
    if vers_minor  < 6:
        print('     please update your python version to 3.6 or later before proceeding with quantumWell')
        print('     exiting from script')
        exit(0)

    print('\ntesting for existence of required modules or packages')
    moduleL = ['sys','os','numpy','matplotlib',
       'PyQt5','scipy']
    modDict = {}
    for mod in moduleL:
        testB = existModule(mod)
        modDict[mod] = testB
    existB = True
    for m,v in modDict.items():
        if v:
            print('     {0:15s}  confirmed'.format(m))
        else:
            print('     {0:15s}  DOES NOT EXIST'.format(m))
            existB = False
    print('\n')
    if not existB:
        print('/n     At least one required package/module is not installed.')
        print('     Install before proceeding with quantumWell.\n')
        print('     exiting script\n')
        exit(0)
