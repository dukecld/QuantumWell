# make qwConfig directory and config file
import sys
from pathlib import Path
import importlib

# #################################################


def makeConfig():
    """ makeConfig creates configuration file for QuantumWell code.

        make directory: $HOME/qwconfig
        make file: $HOME/qwconfig/config
           file contents:
              VERSION=4.0
              path=<path to QuantumWell directory>

        config file makes path info available to other python
        scripts for running QuantumWell scripts and modules
        in any directory.
    """

    VERSION = '4.0'
    confDir = 'qwconfig'
    confstr1 = 'version=' + VERSION
    confstr2 = 'path=' + str(Path.cwd())
    confstr = confstr1 + '\n' + confstr2 + '\n'

    # get paths
    homeP = Path.home()
    cwdP = Path.cwd()

    # set to False to skip name test for directory
    if True:
        testcwd = str(cwdP.name)[0:11]
        if (testcwd != 'QuantumWell'):
            print('must execute this script from directory')
            print('  with name that starts with QuantumWell')
            print('    current directory: ', str(cwdP))
            print('exiting script')
            exit(0)

    pathC = homeP / confDir
    # make confDir if necessary
    if not pathC.exists():
        pathC.mkdir()

    # write config file
    pathF = pathC / 'config'
    print('writing these lines to file ', pathF)
    print('       ', confstr1)
    print('       ', confstr2, '\n')
    pathF.write_text(confstr)
    return

# #################################################


def makeStartScript():
    """ make scripts based on platform os for starting
    quantumWell.py. Copy script to the Desktop directory, but
    can use script in any directory.

    Usage: move start script to any directory, executing the
    script will open the quantumWell GUI in that directory.

    Script created based on platform os:
        Windows: StartQWell.bat
        Macos:   StartQWell.command
        Linux:   StartQWell.sh

    """

    # get path to QuantumWell directory from config is_file
    configP = (Path.home() / 'qwconfig') / 'config'
    if not configP.is_file():
        print('no config file, go to QuantumWell Directory \
        and rerun config script')
        print('   exiting script')
        exit(0)

    with open(configP, mode='r') as fid:
        pathL = [line.strip() for line in fid if
                 line.startswith('path')]
    if len(pathL) != 1:
        print('no path value found in config file')
        print('no script created, ending code')
        return

    pathS = str(pathL[0])
    tmp, pathQ = pathS.split('=')
    pathQ = pathQ.strip()

    # does file exist?
    pathF = Path(pathQ) / 'quantumWell.py'

    if not pathF.is_file():
        print(pathF, ' does not exist, stopping code')
        return

    command = "python " + str(pathF)
    # create start is_file
    platform = sys.platform
    print('creating startfile for platform ', platform)
    cwdP = Path.cwd()
    if platform.startswith('darwin'):
        startfile = Path(cwdP) / 'startQWell.command'
    elif platform.startswith('linux'):
        startfile = Path(cwdP) / 'startQWell.sh'
    elif platform.startswith('win32'):
        startfile = Path(cwdP) / 'startQWell.bat'
    else:
        print('unknown operating system', platform)
        return

    print('    startfile name: ', startfile)

    startfile.touch()
    startfile.write_text(command)
    print('    startfile contains this line')
    print('       ', command)
    startfile.chmod(0o744)

    # copy startfile to desktop
    if (Path.home() / "Desktop").exists():
        dest = Path.home() / "Desktop" / startfile.name
        dest.write_text(startfile.read_text())
        dest.chmod(0o744)
        print('\n    startfile copied to Desktop')
        # shutil.copyfile(src, dst), could use this
    else:
        print('    could not find your Desktop, \
               start file not copied to Desktop')

    print('        can also copy startfile, ', str(dest), ', ')
    print('        to any directory and execute from there')
    print('\nExecute startfile from a terminal or double click ')
    print('    the startfile to open the QuantumWell GUI\n')
    return


def existModule(module):
    """ function to determine if a module or package exists
    Parameter: module - string, e.g. matplotlib
    Returns: True if found, False if not found
    """

    testExist = importlib.util.find_spec(module)
    found = testExist is not None
    return found


def getPythonVersion():
    """ function to obtain current Python version
    Returns: tuple of integers (major version, minor version)
             e.g (3,8) for version 3.8
    """
    vers_major = sys.version_info.major
    vers_minor = sys.version_info.minor
    # vers = str(vers_major) + '.' + str(vers_minor)

    return (vers_major, vers_minor)


if __name__ == "__main__":
    print('\nChecking python version, must be 3.6 or greater')
    versT = getPythonVersion()
    vers_major = versT[0]
    vers_minor = versT[1]
    vers = str(vers_major) + '.' + str(vers_minor)

    print('     you are using python version ', vers)
    if vers_minor < 6:
        print('     please update your python version\
               to 3.6 or later before proceeding with quantumWell')
        print('     exiting from script')
        exit(0)

    print('\ntesting for existence of required modules or packages')
    moduleL = ['numpy', 'matplotlib', 'PyQt5', 'scipy']
    modDict = {}
    for mod in moduleL:
        testB = existModule(mod)
        modDict[mod] = testB
    existB = True
    for m, v in modDict.items():
        if v:
            print('     {0:15s}  confirmed'.format(m))
        else:
            print('     {0:15s}  DOES NOT EXIST'.format(m))
            existB = False
    print('')
    if not existB:
        print('/n     At lea\nst one required\
              package/module is not installed.')
        print('     Install before proceeding with quantumWell.\n')
        print('     exiting script\n')
        exit(0)

    makeConfig()
    makeStartScript()
