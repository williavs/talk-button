# /TALK-BUTTON/

A minimalistic voice-to-text desktop application with built with PyQt6.



[![Email](https://img.shields.io/badge/Email-willy%40v3--ai.com-blue?style=flat-square&logo=gmail)](mailto:willy@v3-ai.com)
[![GitHub](https://img.shields.io/badge/GitHub-williavs-black?style=flat-square&logo=github)](https://github.com/williavs)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-willyv3-0077B5?style=flat-square&logo=linkedin)](https://linkedin.com/in/willyv3)
[![Website](https://img.shields.io/badge/Website-v3--ai.com-green?style=flat-square&logo=safari)](https://v3-ai.com)

![Voice Prompt Screenshot](public/screenshot.png)

## Features

- 🎙️ One-click voice recording
- 🤖 OpenAI Whisper transcription
- ✨ GPT-4o-mini text enhancement
- 🎯 System tray integration
- 🎨 Modern, minimal interface
- ⚡ Fast and responsive
- 🔒 Secure API key storage
- 📝 Customizable system prompts

## Quick Start

1. Download the latest release for macOS
2. Move to Applications folder
3. Right-click > Open
4. Add your OpenAI API key in settings

## Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [API Documentation](docs/API.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Feature Wishlist](docs/WISHLIST.md)

## Requirements

- macOS 10.15 or later
- OpenAI API key
- Microphone access

## Development

```bash
# Clone repository
git clone https://github.com/williavs/talk-button.git
cd talk-button

# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run application
python src/main.py
```

## Building

```bash
# Build macOS application
./build_macos.sh
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for Whisper and GPT-4
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the UI framework
- [PortAudio](http://www.portaudio.com/) for audio handling

## Support

- [GitHub Issues](https://github.com/williavs/talk-button/issues)
- [Documentation](docs/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/voice-prompt)

## Roadmap

See our [Feature Wishlist](docs/WISHLIST.md) for planned improvements.



## Key Features

### Voice Recording
- One-click recording
- Visual feedback
- Automatic silence detection
- High-quality audio capture

### Transcription
- OpenAI Whisper integration
- Multiple language support
- High accuracy
- Fast processing

### Text Enhancement
- GPT-4 post-processing
- Punctuation correction
- Formatting improvement
- Context preservation

### User Interface
- Modern design
- System tray integration
- Drag-and-drop support
- Keyboard shortcuts

### Configuration
- API key management
- Custom system prompts
- Audio settings
- Interface preferences

## Use Cases


1. **AI Prompt Engineering**
   - Rapid prompt iteration
   - Voice-based prompt testing
   - Quick prompt refinement
   - Context preservation

2. **Quick Voice-to-Text**
   - Command line instructions
   - Code comments and TODOs
   - Bug report dictation
   - Quick documentation notes

3. **Development Workflows**
   - Stand-up meeting notes
   - Code review comments
   - Git commit messages
   - Project planning thoughts

## Technical Details

### Architecture
- PyQt6 for UI
- OpenAI API integration
- PortAudio for recording
- Qt's Model-View-Presenter pattern

### Performance
- Optimized audio processing
- Efficient memory usage
- Fast startup time
- Responsive interface

### Security
- Secure API key storage
- Local file handling
- Privacy-focused design
- No data collection


## Version History

See [CHANGELOG.md](CHANGELOG.md) for release notes. 


## Connect With Me

[![Email](https://img.shields.io/badge/Email-willy%40v3--ai.com-blue?style=flat-square&logo=gmail)](mailto:willy@v3-ai.com)
[![GitHub](https://img.shields.io/badge/GitHub-williavs-black?style=flat-square&logo=github)](https://github.com/williavs)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-willyv3-0077B5?style=flat-square&logo=linkedin)](https://linkedin.com/in/willyv3)
[![Website](https://img.shields.io/badge/Website-v3--ai.com-green?style=flat-square&logo=safari)](https://v3-ai.com)