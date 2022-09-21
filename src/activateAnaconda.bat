
set pathOK=abc

set path1=C:%HomePath%\Anaconda3\condabin\activate.bat
set path2=C:\ProgramData\Anaconda3\condabin\activate.bat
if exist %path1% (
	set pathOK=%path1%
)
if exist %path2% (
	set pathOK=%path2%
)

rem is conda and thus anaconda already available
call python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
	echo.
	echo conda path not set
	echo.
	echo found path !pathOK!
	echo running activate.bat file 
	call !pathOK!
	
) else (
	echo we are here here 
	echo conda path already available
	echo ready to call python script
)
