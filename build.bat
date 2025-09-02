@echo off
REM Date Sorter v1.0 - Build Script for Windows
REM This script builds the executable using PyInstaller

echo ========================================
echo    Date Sorter v1.0 - Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python found. Checking version...
python --version

echo.
echo Installing/Updating PyInstaller...
pip install --upgrade pyinstaller

echo.
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo Getting version information...
for /f %%i in ('python -c "import main; print(main.__version__)"') do set VERSION=%%i
echo Version: %VERSION%

echo.
echo Building executable...
python -m PyInstaller --onefile --windowed --name "DateSorter-v%VERSION%" --version-file "version_info.txt" --add-data "logo;logo" --icon=logo/icon.ico main.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\DateSorter-v%VERSION%.exe
echo.
echo You can now distribute DateSorter-v%VERSION%.exe
echo to computers without Python installed.
echo.

REM Show file size
if exist "dist\DateSorter-v%VERSION%.exe" (
    echo File size:
    dir "dist\DateSorter-v%VERSION%.exe" | find "DateSorter-v%VERSION%.exe"
)

echo.
pause
