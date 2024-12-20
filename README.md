# Voice-to-LLM Prompt Refinement

A desktop application that enables voice-to-text transcription and LLM prompt refinement with a modern, dark-themed interface.

## Features

- Real-time voice transcription using OpenAI Whisper
- Dark theme with dynamic recording state feedback
- System tray integration
- Cross-platform compatibility
- Minimal resource footprint

## Prerequisites

- Python 3.10 or higher
- Virtual environment support
- Audio input device (microphone)
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd voice-txt
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python3 -m venv voicetxt_env

# Activate virtual environment
# On Unix/macOS:
source voicetxt_env/bin/activate
# On Windows:
voicetxt_env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

## Usage

Run the application:
```bash
python src/main.py
```

## Development

### Project Structure
```
voice-txt/
├── docs/
│   └── technical_requirements.md
├── src/
│   ├── ui/
│   │   ├── __init__.py
│   │   └── main_window.py
│   └── main.py
├── tests/
├── requirements.txt
└── README.md
```

### Running Tests
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[License Type] - See LICENSE file for details 