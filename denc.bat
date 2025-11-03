@echo off
setlocal enabledelayedexpansion

rem Define the folder path to decrypt (customize as needed)
set "FOLDER_PATH=.\Windows"
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
    rem Call the decryption subroutine
    call :dec
) else (
    echo Folder not found: %FOLDER_PATH%
    pause
    exit /b 1
)

rem Pause and wait for Enter key before exiting
set /p dummy="Decryption process complete. Press Enter to exit..."
exit /b 0

rem Decryption subroutine: Executes the .ps1 and calls Decrypt-Folder
:dec
echo Starting decryption process...
echo This will prompt for the password used during encryption.
powershell.exe -ExecutionPolicy Bypass -Command ^
    "$pass = Read-Host 'Enter decryption password' -AsSecureString; $plainPass = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($pass)); & { . '%SCRIPT_PATH%'; Decrypt-Folder -Path '%FOLDER_PATH%' -Password $plainPass }"

if %errorlevel% == 0 (
    echo Decryption process completed successfully!
) else (
    echo An error occurred during decryption. Check the output above (wrong password?).
)
pause
exit /b 0