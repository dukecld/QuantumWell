@echo off
SETLOCAL enabledelayedexpansion
echo %PATH%
echo.
rem move to activate batch file
call src/activateAnaconda.bat
echo.

echo %PATH%
echo.
echo try to get python version to check path
call python --version
echo.

rem run config.py
call python src\config.py

pause
ENDLOCAL
