@echo off
cd /d "%~dp0"
title KevinNet - Build Windows EXE

echo.
echo =====================================================
echo   KevinNet DNS Config - Windows Build
echo   kevinhaji.com  ^|  kevin.fullstack.dev@gmail.com
echo =====================================================
echo.

python --version
if errorlevel 1 (
    echo [ERROR] Python not found.
    echo Install from https://www.python.org/downloads/windows/
    echo Make sure to check "Add Python to PATH" during install.
    pause & exit /b 1
)

echo [1/3] Installing packages...
python -m pip install dnspython pyinstaller pillow --upgrade --quiet
if errorlevel 1 ( echo [ERROR] pip failed. & pause & exit /b 1 )
echo [OK]
echo.

if not exist "kevinnet.py" (
    echo [ERROR] kevinnet.py not found in this folder.
    pause & exit /b 1
)

echo [2/3] Building EXE...
set ADD_DATA=
if exist "MasterDnsVPN.exe" set ADD_DATA=%ADD_DATA% --add-data "MasterDnsVPN.exe;."
if exist "MasterDnsVPN"     set ADD_DATA=%ADD_DATA% --add-data "MasterDnsVPN;."

python -m PyInstaller --onefile --windowed --name "KevinNet" --clean %ADD_DATA% "kevinnet.py"
if errorlevel 1 ( echo [ERROR] Build failed. & pause & exit /b 1 )

echo.
echo [3/3] Cleanup...
rmdir /s /q "build" 2>nul
del /q "KevinNet.spec" 2>nul

echo.
echo =====================================================
echo   SUCCESS:  dist\KevinNet.exe
echo =====================================================
echo.
explorer "%~dp0dist"
pause
