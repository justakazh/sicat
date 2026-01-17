@echo off
setlocal

echo [*] SICAT Windows Installer

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [-] Python is not installed or not in PATH.
    echo [*] Please install Python 3 from https://www.python.org/downloads/
    pause
    exit /b
)

REM Check for Nmap
where nmap >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Nmap is not installed.
    echo [*] Attempting to install Nmap via Winget...
    winget install Insecure.Nmap
    
    if %errorlevel% neq 0 (
        echo [-] Failed to install Nmap automatically.
        echo [*] Please install Nmap manually from https://nmap.org/download.html
        echo.
    ) else (
        echo [+] Nmap installed successfully.
        echo [*] You might need to restart your terminal for Nmap to work.
    )
) else (
    echo [+] Nmap is already installed.
)

echo.
echo [+] Installing SICAT...
pip install .

if %errorlevel% neq 0 (
    echo.
    echo [-] Failed to install SICAT.
    echo [*] Check if you have pip installed and permissions are correct.
    pause
    exit /b
)

echo.
echo [+] Installation successful!

REM Check if 'sicat' is found in PATH
where sicat >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] 'sicat' command not found in PATH yet.
    echo [*] IMPORTANT: Ensure your Python Scripts folder is in your system PATH.
    echo     Typically: C:\Users\%USERNAME%\AppData\Local\Programs\Python\PythonXX\Scripts
    echo     or: %APPDATA%\Python\PythonXX\Scripts
) else (
    echo [+] 'sicat' command is verified working!
)

echo.
echo [*] Try running: sicat --help
echo.

pause
