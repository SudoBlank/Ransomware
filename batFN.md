Start with; @echo off

To use print statement use; echo

To use a comment use; rem

To pause for sort duration use; pause

To set varible use; set

To set varible and prevent stray spaces use(for paths); set "path="

To use for loops; for %%i in (1 2 3) do ()

To use parameters use; echo arg; %1

To use if loops use; if "%var%"=="value" () else ()

To test exestance of a file use; if exist "C:\file.txt" echo File exists

To use for loops use; for %%f in (*.txt) do echo File: %%f

To read a file; for /f "usebackq delims=" %%A in ("input.txt") do (echo Line: %%A)

To call a Subroutines  use; call ;mysub "hello" echo Back from sub exit /b

To call a function use(after defineing it); call :mysub

To skip a line use; goto skip echo line to skip :skip

To exit code; exit /b 2

To show a error; somecommand if errorlevel 1 (echo somecommand failed with errorlevel >=1)

Other comands(common comands)-echo, set, setlocal, endlocal, if, for, call, goto, exit /b, errorlevel, pause, start, type, find, findstr, copy, move, del, mkdir, rmdir, pushd, popd.

