# Installation Guide

## macOS Installation

### Method 1: Direct Download (Recommended)

1. Download the latest release from the GitHub releases page:
   ```
   https://github.com/williavs/talk-button/releases
   ```

2. Download `Voice-Prompt-Mac.zip`

3. Unzip the file:
   - Double-click the ZIP file
   - Or use Terminal:
     ```bash
     unzip Voice-Prompt-Mac.zip
     ```

4. Move to Applications:
   - Drag "Voice Prompt.app" to Applications folder
   - Or use Terminal:
     ```bash
     mv "Voice Prompt.app" /Applications/
     ```

5. First Launch:
   - Right-click "Voice Prompt.app"
   - Select "Open"
   - Click "Open" in security dialog

6. Grant Permissions:
   - Allow microphone access when prompted
   - System Preferences > Security & Privacy > Microphone
   - Ensure Voice Prompt is checked

### Method 2: Build from Source

#### Prerequisites

1. Install Homebrew:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install Python:
   ```bash
   brew install python@3.11
   ```

3. Install PortAudio:
   ```bash
   brew install portaudio
   ```

#### Building

1. Clone the repository:
   ```bash
   git clone https://github.com/williavs/talk-button.git
   cd talk-button
   ```

2. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Build the application:
   ```bash
   ./build_macos.sh
   ```

5. Install the built application:
   ```bash
   cp -r "dist/Voice Prompt.app" /Applications/
   ```

## Configuration

### OpenAI API Key

1. Get API key from OpenAI:
   - Visit https://platform.openai.com/api-keys
   - Create new API key
   - Copy the key

2. Configure in Voice Prompt:
   - Open Voice Prompt
   - Click settings icon
   - Paste API key
   - Click "Save"

### System Prompt

1. Default location:
   ```
   ~/.voice-prompt/system_prompt
   ```

2. Custom prompt:
   - Open settings
   - Click "System Prompt" tab
   - Edit prompt
   - Click "Save"

## Updating

### App Store Version

1. Open Voice Prompt
2. Check for updates in menu
3. Follow update prompts

### Manual Update

1. Download new version
2. Replace existing app:
   ```bash
   rm -rf "/Applications/Voice Prompt.app"
   mv "Voice Prompt.app" /Applications/
   ```

## Uninstallation

1. Remove application:
   ```bash
   rm -rf "/Applications/Voice Prompt.app"
   ```

2. Remove configuration (optional):
   ```bash
   rm -rf ~/.voice-prompt
   ```

3. Remove cache (optional):
   ```bash
   rm -rf ~/Library/Caches/Voice\ Prompt/
   ```

## Development Setup

1. Install development tools:
   ```bash
   brew install git python@3.11 portaudio
   ```

2. Clone and setup:
   ```bash
   git clone https://github.com/williavs/talk-button.git
   cd talk-button
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run in development:
   ```bash
   python src/main.py
   ```

## Troubleshooting

### Common Issues

1. "App is damaged":
   ```bash
   xattr -cr "/Applications/Voice Prompt.app"
   ```

2. Audio permission issues:
   - System Preferences > Security & Privacy > Microphone
   - Allow Voice Prompt

3. Missing dependencies:
   ```bash
   brew install portaudio
   brew link portaudio
   ```

### Getting Help

1. Check documentation:
   - TROUBLESHOOTING.md
   - GitHub Issues

2. Community support:
   - GitHub Discussions
   - Stack Overflow tags:
     - voice-prompt
     - pyqt6

3. Report bugs:
   - Use GitHub Issues
   - Include system information
   - Provide steps to reproduce 