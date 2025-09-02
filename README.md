# 📁 Date Sorter v1.0 - File Sorting Application

A modern and user-friendly file sorting application. Reorganizes file modification dates starting from 1980, incrementing by one day for each file.

## 🎯 Version 1.0 Features

- ✅ **Standalone Executable**: No Python installation required
- ✅ **Cross-Platform**: Windows, macOS, and Linux support
- ✅ **Modern GUI**: Dark theme with responsive design
- ✅ **Custom Logo**: Professional branding with custom icon
- ✅ **Drag & Drop**: Intuitive file reordering
- ✅ **Multi-Selection**: Ctrl+click and Shift+click support
- ✅ **Progress Tracking**: Real-time operation status
- ✅ **Custom Start Year**: Configurable date assignment

## ✨ Features

- **Modern GUI**: Tkinter-based user-friendly interface
- **Folder Selection**: Choose any folder and view its files
- **Detailed Information**: File name, size, and modification date in table format
- **Drag & Drop**: Reorder files by dragging them in the table
- **Multi-Selection**: Select multiple files using Ctrl key
- **Range Selection**: Select file ranges using Shift key
- **Automatic Sorting**: Automatically organize dates starting from 1980
- **Progress Tracking**: Track progress with progress bar during operations
- **Customizable Start Year**: Configure the starting year for date assignment
- **Dark Theme**: Eye-friendly dark color scheme
- **Header Sorting**: Sort by any column (A-Z/Z-A, numerical, chronological)

## 🚀 Installation

### Option 1: Standalone Executable (Recommended)
1. Download `DateSorter-v1.0.0.exe` (Windows) or `DateSorter-v1.0.0` (Linux/Mac)
2. Double-click to run - **No Python installation required!**

### Option 2: From Source Code
#### Requirements
- Python 3.7 or higher
- Windows, macOS, or Linux

#### Installation Steps
1. Clone or download the project
2. Open Terminal/Command Prompt
3. Navigate to the project directory:
   ```bash
   cd Date-Sorter
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python main.py
   ```

### Building Executable from Source
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Run build script:
   - **Windows**: Double-click `build.bat`
   - **Linux/Mac**: Run `./build.sh`
3. Find executable in `dist/` folder with version in filename:
   - **Windows**: `DateSorter-v1.0.0.exe`
   - **Linux/Mac**: `DateSorter-v1.0.0`

**Note**: If you get "pyinstaller not found" error, use `python -m PyInstaller` instead of `pyinstaller` directly.

## 📖 Usage

### 1. Folder Selection
- Click the "📂 Browse" button
- Select the folder you want to sort
- Files will automatically appear in the table

### 2. File Sorting
- Drag files in the table to reorder them
- Use Ctrl key to select multiple files
- Use Shift key to select file ranges
- Click "🔄 Update Dates" button

### 3. Date Modification
- Configure the starting year (default: 1980)
- Click "🔄 Update Dates" button
- Operation will start automatically
- All files will be dated starting from the specified year, incrementing by one day

## 📁 Project Structure

```
Date-Sorter/
├── main.py              # Main application file
├── ui.py                # User interface
├── sorter.py            # File operations and date calculations
├── logo/                # Logo and icon files
│   ├── logo.png         # Main logo image
│   ├── favicon.ico      # Original favicon
│   ├── icon.ico         # Generated executable icon
│   └── favicon-32x32.png # 32x32 logo
├── requirements.txt     # Python dependencies
├── version_info.txt     # Version information for executable
├── build.bat            # Windows build script
├── build.sh             # Linux/Mac build script
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🔧 Technical Details

### Technologies Used
- **Python 3.7+**: Main programming language
- **Tkinter**: GUI framework
- **PyInstaller**: Executable creation
- **Pillow**: Image processing for icons
- **Threading**: For asynchronous operations
- **OS Module**: File system operations
- **DateTime**: Date calculations

### File Operations
- File sizes are automatically formatted (B, KB, MB, GB, TB)
- Modification dates are displayed in readable format
- Compatible with Windows and Unix systems

### Security
- Confirmation dialog before operations
- File permissions are checked
- User is informed in case of errors

## ⚠️ Important Notes

- **Irreversible**: Date modification operations cannot be undone
- **Backup**: Always backup your important files before processing
- **Permissions**: Write permission to the folder is required
- **Files Only**: Folders are not included in the process

## 🐛 Troubleshooting

### Common Issues

**"No access permission to folder" error:**
- Check folder permissions
- Try running as administrator

**"File date could not be changed" error:**
- Ensure the file is not being used by another program
- Check file permissions

**Application won't start:**
- Make sure Python 3.7+ is installed
- Check that Tkinter module is installed

## 📝 License

This project is developed for educational purposes. You can freely use and modify it.

## 🤝 Contributing

1. Fork the project
2. Create a new feature branch (`git checkout -b new-feature`)
3. Commit your changes (`git commit -am 'New feature added'`)
4. Push your branch (`git push origin new-feature`)
5. Create a Pull Request

## 📞 Contact

You can open an issue for questions or send a pull request.

## 👨‍💻 Author

**Author:** Semi Eren Gökyıldız
- **Email:** [gokyildizsemieren@gmail.com](mailto:gokyildizsemieren@gmail.com)
- **GitHub:** [SERENGOKYILDIZ](https://github.com/SERENGOKYILDIZ)
- **LinkedIn:** [Semi Eren Gökyıldız](https://www.linkedin.com/in/semi-eren-gokyildiz/)

---

**Note**: This application permanently modifies file dates. Always backup your important files before processing!