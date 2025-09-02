# 🔨 Build Instructions - Date Sorter v1.0

This document explains how to build the Date Sorter executable from source code.

## 📋 Prerequisites

### Required Software
- **Python 3.7+** (Download from [python.org](https://python.org))
- **pip** (usually comes with Python)
- **Pillow** (for image processing and icon conversion)
- **Git** (optional, for cloning repository)

### System Requirements
- **Windows**: Windows 7 or later
- **macOS**: macOS 10.12 or later  
- **Linux**: Most modern distributions

## 🚀 Quick Build (Automated)

### Windows
1. Open Command Prompt or PowerShell
2. Navigate to project directory:
   ```cmd
   cd path\to\Date-Sorter
   ```
3. Run build script:
   ```cmd
   build.bat
   ```

### Linux/macOS
1. Open Terminal
2. Navigate to project directory:
   ```bash
   cd path/to/Date-Sorter
   ```
3. Make script executable and run:
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

## 🔧 Manual Build Process

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: Pillow is required for icon processing. If you encounter icon-related errors, install it separately:
```bash
pip install Pillow
```

### Step 2: Clean Previous Builds
```bash
# Windows
rmdir /s /q dist build

# Linux/macOS
rm -rf dist build
```

### Step 3: Build Executable
```bash
# Windows (with version in filename and custom icon)
python -m PyInstaller --onefile --windowed --name "DateSorter-v1.0.0" --version-file "version_info.txt" --add-data "logo;logo" --icon=logo/icon.ico main.py

# Linux/macOS (with version in filename and custom icon)
python3 -m PyInstaller --onefile --windowed --name "DateSorter-v1.0.0" --version-file "version_info.txt" --add-data "logo:logo" --icon=logo/icon.ico main.py
```

### Step 4: Find Your Executable
- **Windows**: `dist\DateSorter-v1.0.0.exe`
- **Linux/macOS**: `dist\DateSorter-v1.0.0`

## 📊 Build Options Explained

### PyInstaller Flags
- `--onefile`: Creates a single executable file
- `--windowed`: No console window (GUI only)
- `--name "DateSorter"`: Sets executable name
- `--version-file "version_info.txt"`: Adds version information

### Advanced Options
```bash
# With custom icon and logo data
python -m PyInstaller --onefile --windowed --icon=logo/icon.ico --add-data "logo;logo" --name "DateSorter-v1.0.0" main.py

# With UPX compression (smaller file size)
python -m PyInstaller --onefile --windowed --upx-dir=/path/to/upx --icon=logo/icon.ico --name "DateSorter-v1.0.0" main.py

# Debug build (with console)
python -m PyInstaller --onefile --console --icon=logo/icon.ico --name "DateSorter-v1.0.0" main.py
```

## 🐛 Troubleshooting

### Common Issues

**"PyInstaller not found" or "pyinstaller is not recognized"**
```bash
# Install PyInstaller
pip install --upgrade pyinstaller

# Use python -m PyInstaller instead of pyinstaller directly
python -m PyInstaller --version
```

**"Icon format error" or "PIL not found"**
```bash
# Install Pillow for image processing
pip install Pillow

# Or install from requirements
pip install -r requirements.txt
```

**"Permission denied" (Linux/macOS)**
```bash
chmod +x build.sh
```

**"Build failed"**
- Check Python version: `python --version`
- Update pip: `pip install --upgrade pip`
- Clear cache: `pip cache purge`

**"Executable too large"**
- Use UPX compression
- Exclude unnecessary modules in spec file
- Use `--exclude-module` flag

### File Size Optimization
```bash
# Exclude large modules
python -m PyInstaller --onefile --windowed --exclude-module matplotlib --exclude-module numpy --name "DateSorter-v1.0.0" main.py
```

## 📦 Distribution

### Windows
- Distribute `DateSorter-v1.0.0.exe`
- No additional files needed
- Works on Windows 7+

### Linux
- Distribute `DateSorter-v1.0.0` executable
- May need to set executable permissions: `chmod +x DateSorter-v1.0.0`
- Test on target distribution

### macOS
- Distribute `DateSorter-v1.0.0` executable
- May need to sign for distribution outside App Store
- Test on target macOS version

## 🔍 Testing Your Build

1. **Basic Test**: Run executable on same machine
2. **Clean Test**: Test on machine without Python
3. **Different OS**: Test on different operating system
4. **File Operations**: Test folder selection and date modification
5. **Error Handling**: Test with invalid inputs

## 📝 Version Information

The executable includes version information from `version_info.txt`:
- File version: 1.0.0.0
- Product version: 1.0.0.0
- Company: Semi Eren Gökyıldız
- Description: Date Sorter - File Date Management Tool

## 🆘 Support

If you encounter issues:
1. Check this troubleshooting guide
2. Verify Python and pip versions
3. Try clean build (delete dist/build folders)
4. Check PyInstaller documentation
5. Open an issue on GitHub

---

**Happy Building! 🎉**
