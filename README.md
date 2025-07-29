# PDF Repeat

A Python application for repeating and merging PDF files with different modes.

## Features

- **Single File Repeat**: Repeat each PDF file individually
- **Merge Then Repeat**: Merge all PDFs first, then repeat the merged result
- **Page Repeat Merge**: Repeat each page of each PDF, then merge

## Usage

1. Run the application
2. Select PDF files to process
3. Enter the number of repetitions
4. Choose the repeat mode
5. Select output location

## Building from Source

### Prerequisites
- Python 3.9+
- pip

### Installation
```bash
git clone https://github.com/yourusername/pdf-repeat.git
cd pdf-repeat
pip install -r requirements.txt
python main.py
```

### Building Executables
```bash
pip install pyinstaller
pyinstaller pdf-repeat.spec
```

The executable will be created in the `dist/` folder.

## Automated Builds

This project uses GitHub Actions to automatically build executables for:
- Windows (x64)
- macOS (x64)

Builds are triggered on:
- Push to main/master branch
- Pull requests
- Release creation

## Download

Download the latest release from the [Releases](https://github.com/yourusername/pdf-repeat/releases) page.

## Requirements

- PyPDF2==3.0.1
