# Development Guide

## Project Structure

```
voice-txt/
├── src/                    # Source code
│   ├── core/              # Core functionality
│   │   ├── audio_recorder.py  # Audio recording functionality
│   │   └── transcription.py   # OpenAI integration and transcription
│   ├── ui/                # User interface components
│   │   ├── components/    # Reusable UI components
│   │   └── main_window.py # Main application window
│   └── main.py           # Application entry point
├── public/               # Public assets
├── build_macos.sh       # macOS build script
├── setup.py             # Build configuration
└── requirements.txt     # Python dependencies
```

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/williavs/talk-button.git
cd talk-button
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application in development mode:
```bash
python src/main.py
```

## Architecture Overview

### Core Components

1. **TranscriptionService** (`src/core/transcription.py`)
   - Handles OpenAI API integration
   - Manages API key storage and retrieval
   - Processes audio transcriptions
   - Post-processes text using GPT-4

2. **AudioRecorder** (`src/core/audio_recorder.py`)
   - Manages audio recording
   - Handles temporary file management
   - Provides audio format conversion

### UI Components

1. **MainWindow** (`src/ui/main_window.py`)
   - Main application window
   - Manages window state and behavior
   - Handles drag-and-drop functionality

2. **SystemTray** (`src/ui/components/system_tray.py`)
   - System tray integration
   - Application menu
   - Quick access controls

3. **SettingsDialog** (`src/ui/components/settings_dialog.py`)
   - API key configuration
   - System prompt customization
   - Application preferences

## Building and Distribution

### macOS Build Process

1. The build process is handled by `build_macos.sh`:
   - Creates a virtual environment
   - Installs dependencies
   - Packages the application using py2app
   - Creates a distributable ZIP file

2. Build the application:
```bash
./build_macos.sh
```

### Known Issues and Solutions

1. **libportaudio Dependency**
   - The application requires libportaudio for audio recording
   - Currently handled by copying from Homebrew location
   - Future improvement: Bundle libportaudio more elegantly

2. **Application Bundle Permissions**
   - First-time users need to right-click and select "Open"
   - Add to Security & Privacy settings on macOS

## Adding New Features

### Integration Points

1. **Audio Processing**
   - Extend `AudioRecorder` class
   - Add new audio formats or processing methods
   - Implement noise reduction or filtering

2. **Transcription Service**
   - Add alternative AI providers
   - Implement custom post-processing
   - Add language support

3. **User Interface**
   - Create new UI components in `src/ui/components`
   - Follow Qt's Model-View-Presenter pattern
   - Use PyQt6's signal-slot mechanism

### Best Practices

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Document public methods and classes

2. **Error Handling**
   - Use try-except blocks for external services
   - Provide user-friendly error messages
   - Log errors for debugging

3. **Testing**
   - Write unit tests for core functionality
   - Mock external services
   - Test UI components with QTest

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Resources

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Python Audio Processing](https://python-sounddevice.readthedocs.io/) 