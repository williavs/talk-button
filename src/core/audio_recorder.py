import pyaudio
import wave
import numpy as np
from pathlib import Path
from typing import Optional
from datetime import datetime

class AudioRecorder:
    """Handles audio recording functionality using PyAudio."""
    
    CHUNK = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 16000  # Compatible with Whisper's expected sample rate
    
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        self.frames: list[bytes] = []
        self.is_recording = False
        self._setup_temp_dir()
    
    def _setup_temp_dir(self) -> None:
        """Create temporary directory for audio files if it doesn't exist."""
        self.temp_dir = Path(__file__).parent.parent.parent / "temp"
        self.temp_dir.mkdir(exist_ok=True)
        # Clean up any existing temporary files
        for file in self.temp_dir.glob("*.wav"):
            try:
                file.unlink()
            except Exception:
                pass
    
    def start_recording(self) -> None:
        """Start recording audio from the microphone."""
        if self.is_recording:
            return
            
        self.frames = []
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self._audio_callback
        )
        self.is_recording = True
        self.stream.start_stream()
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback function for audio stream processing."""
        if status:
            print(f"Audio stream status: {status}")
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)
    
    def stop_recording(self) -> Optional[Path]:
        """Stop recording and save the audio file."""
        if not self.is_recording:
            print("Warning: stop_recording called but not recording")
            return None
            
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
        if not self.frames:
            print("Warning: No audio frames recorded")
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.temp_dir / f"recording_{timestamp}.wav"
        
        # Convert float32 audio to int16 for better compatibility
        try:
            print(f"Processing {len(self.frames)} audio frames...")
            float_data = np.frombuffer(b''.join(self.frames), dtype=np.float32)
            int_data = (float_data * 32767).astype(np.int16)
            
            print(f"Saving audio to {output_path}")
            with wave.open(str(output_path), 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(2)  # 16-bit audio
                wf.setframerate(self.RATE)
                wf.writeframes(int_data.tobytes())
            
            print(f"Audio saved successfully. File size: {output_path.stat().st_size} bytes")
            return output_path
            
        except Exception as e:
            print(f"Error saving audio file: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return None
    
    def cleanup(self) -> None:
        """Clean up resources."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        
        # Clean up temporary files
        for file in self.temp_dir.glob("*.wav"):
            try:
                file.unlink()
            except Exception:
                pass
        
    def __del__(self):
        """Ensure resources are cleaned up."""
        self.cleanup()