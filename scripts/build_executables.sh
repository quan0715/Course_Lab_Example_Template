#!/usr/bin/env bash

# Build script for creating standalone executables for all platforms
# This script uses PyInstaller to package run_tests.py into executables

set -e

# Change to project root directory (parent of scripts/)
cd "$(dirname "$0")/.."

echo "🔧 Build Executables Script"
echo "=========================================="

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller not found!"
    echo "Please install it with: pip install pyinstaller"
    exit 1
fi

echo "✅ PyInstaller found"

# Create dist directory if it doesn't exist
mkdir -p dist

echo ""
echo "Building executables for all platforms..."
echo "=========================================="

# Determine the path separator based on the current OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    SEP=";"
else
    SEP=":"
fi

# Build for Linux
echo ""
echo "📦 Building for Linux..."
pyinstaller --onefile \
    --name run_tests_linux \
    --add-data "templates${SEP}templates" \
    run_tests.py

# Build for Windows
echo ""
echo "📦 Building for Windows..."
pyinstaller --onefile \
    --name run_tests.exe \
    --add-data "templates${SEP}templates" \
    run_tests.py

# Build for macOS
echo ""
echo "📦 Building for macOS..."
pyinstaller --onefile \
    --name run_tests_mac \
    --add-data "templates${SEP}templates" \
    run_tests.py

echo ""
echo "=========================================="
echo "✅ Build complete!"
echo ""
echo "Executables created in dist/ directory:"
echo "  - dist/run_tests_linux (Linux)"
echo "  - dist/run_tests.exe (Windows)"
echo "  - dist/run_tests_mac (macOS)"
echo ""
echo "Note: These executables are built for the current platform's"
echo "architecture. For true cross-platform builds, you need to"
echo "build on each target platform separately."
echo "=========================================="
