from setuptools import setup, find_packages
import os
import shutil

def copy_dylib():
    """Copy libportaudio to the current directory."""
    src = '/opt/homebrew/lib/libportaudio.2.dylib'
    dst = 'libportaudio.2.dylib'
    if os.path.exists(src):
        shutil.copy2(src, dst)
        return dst
    return None

APP = ['src/main.py']
DATA_FILES = []

# Add profile picture if it exists
if os.path.exists('public/profile.jpeg'):
    DATA_FILES.append(('public', ['public/profile.jpeg']))

# Add app icon if it exists
if os.path.exists('public/app_icon.icns'):
    DATA_FILES.append(('public', ['public/app_icon.icns']))

# Copy and add libportaudio
dylib_path = copy_dylib()
if dylib_path:
    DATA_FILES.append(('Frameworks', [dylib_path]))

OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'PyQt6',
        'openai',
        'numpy',
        'pyaudio',
        'pyperclip',
        'dotenv',
        'sounddevice',
        'soundfile',
        'src',
        'src.ui',
        'src.core',
        'src.utils',
    ],
    'includes': [
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'numpy.core._methods',
        'numpy.lib.format',
        'src.ui.main_window',
        'src.ui.components',
        'src.core.transcription',
        'src.core.audio_recorder',
    ],
    'excludes': ['tkinter', 'matplotlib'],
    'iconfile': 'public/app_icon.icns' if os.path.exists('public/app_icon.icns') else None,
    'plist': {
        'CFBundleName': 'Voice Prompt',
        'CFBundleDisplayName': 'Voice Prompt',
        'CFBundleIdentifier': 'com.v3-ai.voiceprompt',
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'LSMinimumSystemVersion': '10.15',
        'NSMicrophoneUsageDescription': 'Voice Prompt needs access to your microphone to record audio for transcription.',
        'NSHighResolutionCapable': True,
        'LSApplicationCategoryType': 'public.app-category.productivity',
    }
}

setup(
    name='Voice Prompt',
    version='1.0.0',
    author='William Van Sickle',
    description='Voice-to-text application with OpenAI integration',
    app=APP,
    data_files=DATA_FILES,
    packages=find_packages(),
    include_package_data=True,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 