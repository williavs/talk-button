# API Documentation

## Core Components

### TranscriptionService

The `TranscriptionService` class handles all interactions with OpenAI's API and manages transcription functionality.

```python
class TranscriptionService:
    def __init__(self):
        """Initialize the transcription service."""
        self.api_key = None
        self.client = None
        self._load_api_key()
```

#### Methods

##### API Key Management

```python
def _load_api_key(self) -> Optional[str]:
    """
    Load the API key from the config file.
    
    Returns:
        str | None: The API key if found, None otherwise.
    """

def load_api_key(self) -> Optional[str]:
    """
    Public method to load and return the API key.
    
    Returns:
        str | None: The API key if found, None otherwise.
    """

def clear_api_key(self) -> bool:
    """
    Clear the API key from local storage.
    
    Returns:
        bool: True if successful, False otherwise.
    """
```

##### Transcription

```python
def transcribe_audio(self, audio_path: Path) -> str:
    """
    Transcribe audio file using OpenAI's Whisper API.
    
    Args:
        audio_path (Path): Path to the audio file.
    
    Returns:
        str: Transcribed text or error message.
    """

def post_process_transcript(self, transcript: str) -> str:
    """
    Post-process transcription using GPT-4.
    
    Args:
        transcript (str): Raw transcription text.
    
    Returns:
        str: Processed text with improved formatting.
    """
```

### AudioRecorder

The `AudioRecorder` class manages audio recording and temporary file handling.

```python
class AudioRecorder:
    def __init__(self):
        """Initialize the audio recorder."""
        self.stream = None
        self.frames = []
        self.is_recording = False
```

#### Methods

##### Recording Control

```python
def start_recording(self) -> None:
    """
    Start recording audio.
    
    Raises:
        AudioDeviceError: If no audio device is available.
    """

def stop_recording(self) -> Path:
    """
    Stop recording and save the audio file.
    
    Returns:
        Path: Path to the saved audio file.
    
    Raises:
        AudioSaveError: If saving the file fails.
    """

def is_recording(self) -> bool:
    """
    Check if recording is in progress.
    
    Returns:
        bool: True if recording, False otherwise.
    """
```

## UI Components

### MainWindow

The main application window that handles user interactions and displays the interface.

```python
class MainWindow(QMainWindow):
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.transcription_service = TranscriptionService()
        self.audio_recorder = AudioRecorder()
```

#### Signals

```python
# Recording state changed
recording_started = Signal()
recording_stopped = Signal()

# Transcription events
transcription_started = Signal()
transcription_completed = Signal(str)
transcription_failed = Signal(str)
```

#### Methods

```python
def toggle_recording(self) -> None:
    """Toggle audio recording state."""

def handle_transcription(self, text: str) -> None:
    """
    Handle transcribed text.
    
    Args:
        text (str): Transcribed text to process.
    """

def show_settings(self) -> None:
    """Show the settings dialog."""
```

### SettingsDialog

Dialog for configuring application settings.

```python
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        """Initialize the settings dialog."""
        super().__init__(parent)
        self.transcription_service = parent.transcription_service
```

#### Signals

```python
# Settings changed
api_key_changed = Signal(str)
system_prompt_changed = Signal(str)
```

#### Methods

```python
def save_api_key(self) -> None:
    """Save the API key to configuration."""

def load_system_prompt(self) -> str:
    """
    Load the system prompt from configuration.
    
    Returns:
        str: The system prompt text.
    """

def save_system_prompt(self) -> None:
    """Save the system prompt to configuration."""
```

## Configuration

### File Locations

```python
# API Key
~/.voice-prompt/config

# System Prompt
~/.voice-prompt/system_prompt

# Temporary Files
~/Library/Caches/Voice Prompt/
```

### Configuration Format

#### API Key
```text
sk-your-api-key-here
```

#### System Prompt
```text
You are a helpful assistant. Your task is to correct any spelling discrepancies 
in the transcribed text. Add necessary punctuation such as periods, commas, 
and capitalization. Make the text more readable while preserving its original meaning.
```

## Error Handling

### Custom Exceptions

```python
class AudioDeviceError(Exception):
    """Raised when audio device is not available."""
    pass

class TranscriptionError(Exception):
    """Raised when transcription fails."""
    pass

class ConfigurationError(Exception):
    """Raised when configuration is invalid."""
    pass
```

### Error Codes

```python
ERROR_CODES = {
    'E001': 'Audio device not found',
    'E002': 'API key not configured',
    'E003': 'Network error',
    'E004': 'Transcription failed',
    'E005': 'File access error'
}
```

## Integration Examples

### Basic Usage

```python
from src.core.transcription import TranscriptionService
from src.core.audio_recorder import AudioRecorder

# Initialize services
transcription = TranscriptionService()
recorder = AudioRecorder()

# Record and transcribe
recorder.start_recording()
# ... wait for recording ...
audio_file = recorder.stop_recording()
text = transcription.transcribe_audio(audio_file)
```

### Custom Post-processing

```python
class CustomTranscriptionService(TranscriptionService):
    def post_process_transcript(self, transcript: str) -> str:
        # Custom processing logic
        processed = super().post_process_transcript(transcript)
        return processed.upper()  # Convert to uppercase
```

### Event Handling

```python
class CustomWindow(MainWindow):
    def __init__(self):
        super().__init__()
        self.recording_started.connect(self.on_recording_start)
        self.transcription_completed.connect(self.on_transcription_done)
    
    def on_recording_start(self):
        print("Recording started")
    
    def on_transcription_done(self, text: str):
        print(f"Transcription: {text}")
``` 