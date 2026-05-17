import unittest
from unittest.mock import patch, MagicMock
from app.services.whisper_service import whisper_service

class TestWhisperService(unittest.TestCase):
    @patch('app.services.whisper_service.subprocess.run')
    @patch('app.services.whisper_service.Path.exists')
    def test_extract_audio_not_exists(self, mock_exists, mock_run):
        # Audio file does not exist, should trigger ffmpeg
        mock_exists.return_value = False
        
        result = whisper_service._extract_audio('video.mp4', 'vid123')
        
        mock_run.assert_called_once()
        self.assertTrue('storage/audio/vid123.mp3' in result)

    @patch('app.services.whisper_service.subprocess.run')
    @patch('app.services.whisper_service.Path.exists')
    def test_extract_audio_already_exists(self, mock_exists, mock_run):
        # Audio file exists, should NOT trigger ffmpeg
        mock_exists.return_value = True
        
        result = whisper_service._extract_audio('video.mp4', 'vid123')
        
        mock_run.assert_not_called()
        self.assertTrue('storage/audio/vid123.mp3' in result)

    @patch.object(whisper_service, '_extract_audio')
    @patch.object(whisper_service, '_get_model')
    def test_transcribe(self, mock_get_model, mock_extract_audio):
        mock_extract_audio.return_value = 'audio.mp3'
        
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {
            'segments': [{'start': 0.0, 'end': 2.0, 'text': 'Hello world'}]
        }
        mock_get_model.return_value = mock_model
        
        result = whisper_service.transcribe('video.mp4', 'vid123')
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['text'], 'Hello world')
