import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from src.core.transcription import TranscriptionService

@pytest.fixture
def mock_openai():
    with patch('src.core.transcription.OpenAI') as mock:
        yield mock

@pytest.fixture
def transcription_service(mock_openai):
    mock_openai.return_value.api_key = 'test_key'
    return TranscriptionService()

def test_transcription_service_initialization(mock_openai):
    """Test that TranscriptionService initializes correctly with API key."""
    mock_openai.return_value.api_key = 'test_key'
    service = TranscriptionService()
    assert service.client is not None

def test_transcription_service_initialization_no_api_key(mock_openai):
    """Test that TranscriptionService raises error without API key."""
    mock_openai.return_value.api_key = None
    with pytest.raises(ValueError):
        TranscriptionService()

def test_transcribe_audio_success(transcription_service, tmp_path):
    """Test successful audio transcription."""
    # Create a dummy audio file
    audio_path = tmp_path / "test.wav"
    audio_path.write_bytes(b"dummy audio content")
    
    # Mock the transcription response
    mock_response = "Test transcription"
    transcription_service.client.audio.transcriptions.create.return_value = mock_response
    
    result = transcription_service.transcribe_audio(audio_path)
    assert result == mock_response

def test_refine_prompt_success(transcription_service):
    """Test successful prompt refinement."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Refined test prompt"
    transcription_service.client.chat.completions.create.return_value = mock_response
    
    result = transcription_service.refine_prompt("Test prompt")
    assert result == "Refined test prompt" 