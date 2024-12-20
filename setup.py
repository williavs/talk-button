from setuptools import setup
import os

APP = ['src/main.py']
DATA_FILES = []

# Add profile picture if it exists
if os.path.exists('public/profile.jpeg'):
    DATA_FILES.append(('public', ['public/profile.jpeg']))

# Add app icon if it exists
if os.path.exists('public/app_icon.icns'):
    DATA_FILES.append(('public', ['public/app_icon.icns']))

# Add libportaudio if it exists
if os.path.exists('/opt/homebrew/lib/libportaudio.2.dylib'):
    DATA_FILES.append(('lib', ['/opt/homebrew/lib/libportaudio.2.dylib']))

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
    ],
    'includes': [
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'numpy.core._methods',
        'numpy.lib.format',
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
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 