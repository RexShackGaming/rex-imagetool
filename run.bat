@echo off
setlocal

rem --- Check if Python is installed ---
where python >nul 2>&1
if errorlevel 1 (
    echo Python was not found on this computer.
    where winget >nul 2>&1
    if errorlevel 1 (
        echo Could not find winget to install Python automatically.
        echo Please install Python from https://www.python.org/downloads/ ^(check "Add python.exe to PATH" during setup^), then run this again.
        pause
        exit /b 1
    )
    echo Installing Python via winget, please wait...
    winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    if errorlevel 1 (
        echo Automatic install failed. Please install Python manually from https://www.python.org/downloads/ ^(check "Add python.exe to PATH" during setup^), then run this again.
        pause
        exit /b 1
    )
    echo Python installed. Please close this window and run run.bat again so the new PATH takes effect.
    pause
    exit /b 0
)

rem --- Check if Pillow is installed, install if missing ---
python -m pip show pillow >nul 2>&1
if errorlevel 1 (
    echo Installing required package: Pillow...
    python -m pip install --user Pillow
)

python bulk_resize.py
pause
