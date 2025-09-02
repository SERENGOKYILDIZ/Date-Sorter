#!/bin/bash
# Date Sorter v1.0 - Build Script for Linux/Mac
# This script builds the executable using PyInstaller

echo "========================================"
echo "   Date Sorter v1.0 - Build Script"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "Python found. Checking version..."
python3 --version

echo
echo "Installing/Updating PyInstaller..."
pip3 install --upgrade pyinstaller

echo
echo "Cleaning previous builds..."
rm -rf dist build *.spec

echo
echo "Getting version information..."
VERSION=$(python3 -c "import main; print(main.__version__)")
echo "Version: $VERSION"

echo
echo "Building executable..."
python3 -m PyInstaller --onefile --windowed --name "DateSorter-v$VERSION" --version-file "version_info.txt" --add-data "logo:logo" --icon=logo/icon.ico main.py

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Build failed!"
    echo "Check the error messages above."
    exit 1
fi

echo
echo "========================================"
echo "   Build completed successfully!"
echo "========================================"
echo
echo "Executable location: dist/DateSorter-v$VERSION"
echo
echo "You can now distribute DateSorter-v$VERSION"
echo "to computers without Python installed."
echo

# Show file size
if [ -f "dist/DateSorter-v$VERSION" ]; then
    echo "File size:"
    ls -lh "dist/DateSorter-v$VERSION"
fi

echo
