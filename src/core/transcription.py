import os
from pathlib import Path
from openai import OpenAI

class TranscriptionService:
    def __init__(self):
        self.api_key = None
        self.client = None
        self._load_api_key()
        
    def _load_api_key(self):
        """Load the API key from config file without initializing the client."""
        try:
            home = str(Path.home())
            config_dir = os.path.join(home, '.voice-prompt')
            config_file = os.path.join(config_dir, 'config')
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    api_key = f.read().strip()
                    if api_key:
                        self.api_key = api_key
            return self.api_key
        except Exception as e:
            print(f"Error loading API key: {e}")
            return None

    def _load_system_prompt(self) -> str:
        """Load the system prompt from config file."""
        try:
            home = str(Path.home())
            config_dir = os.path.join(home, '.voice-prompt')
            prompt_file = os.path.join(config_dir, 'system_prompt')
            if os.path.exists(prompt_file):
                with open(prompt_file, 'r') as f:
                    return f.read().strip()
        except Exception as e:
            print(f"Error loading system prompt: {e}")
        
        # Return default prompt if file doesn't exist or there's an error
        return """You are a helpful assistant. Your task is to correct any spelling discrepancies 
in the transcribed text. Add necessary punctuation such as periods, commas, 
and capitalization. Make the text more readable while preserving its original meaning. 
Use only the context provided."""

    def load_api_key(self):
        """Public method to load API key and return it."""
        return self._load_api_key()

    def clear_api_key(self) -> bool:
        """Clear the API key from local storage."""
        try:
            home = str(Path.home())
            config_dir = os.path.join(home, '.voice-prompt')
            config_file = os.path.join(config_dir, 'config')
            
            if os.path.exists(config_file):
                os.remove(config_file)
                self.api_key = None
                self.client = None
                print("API key cleared successfully")
                return True
            return False
        except Exception as e:
            print(f"Error clearing API key: {e}")
            return False

    def _ensure_client(self):
        """Initialize the OpenAI client if we have an API key."""
        if self.api_key and not self.client:
            try:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.openai.com/v1"  # Explicitly set base URL
                )
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
                return False
        return self.client is not None

    def post_process_transcript(self, transcript: str) -> str:
        """Post-process the transcript using GPT-4 for improved accuracy."""
        if not self._ensure_client():
            return transcript

        system_prompt = self._load_system_prompt()

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": transcript
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Post-processing error: {e}")
            return transcript

    def transcribe_audio(self, audio_path: Path) -> str:
        """Transcribe audio and post-process the result."""
        try:
            if not self._ensure_client():
                print("Error: OpenAI client initialization failed")
                return "Error: OpenAI API key not found. Please set it in the settings."

            if not audio_path.exists():
                print(f"Error: Audio file not found at {audio_path}")
                return "Error: Audio file not found"

            print(f"Attempting to transcribe audio file: {audio_path}")
            print(f"File size: {audio_path.stat().st_size} bytes")

            with open(audio_path, "rb") as audio_file:
                print("Starting transcription with Whisper...")
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text",
                    language="en"
                )
                print(f"Whisper transcription completed: {transcript[:100]}...")
                
                # Post-process the transcript
                if transcript:
                    print("Starting GPT-4 post-processing...")
                    return self.post_process_transcript(transcript)
                return transcript

        except Exception as e:
            print(f"Transcription error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return f"Error: {str(e)}"
