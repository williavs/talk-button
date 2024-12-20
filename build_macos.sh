#!/bin/bash

# Exit on error
set -e

echo "🚀 Building Voice Prompt for macOS..."

# Ensure we're in the project root
cd "$(dirname "$0")"

# Create and activate virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv build_env
source build_env/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Build the application
echo "🔨 Building application..."
python setup.py py2app

# Create ZIP for distribution
echo "📦 Creating ZIP archive..."
cd dist
zip -r "Voice-Prompt-Mac.zip" "Voice Prompt.app"
cd ..

# Deactivate virtual environment
deactivate

echo "✨ Build complete!"
echo "📁 Application bundle is in: dist/Voice Prompt.app"
echo "📦 ZIP archive is in: dist/Voice-Prompt-Mac.zip"

echo "
📝 Distribution Instructions:
1. Upload Voice-Prompt-Mac.zip to your website
2. Users can download and unzip
3. First time running: Users should right-click > Open
4. Add instructions for users to allow app in System Preferences > Security & Privacy
" 