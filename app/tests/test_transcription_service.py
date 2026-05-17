import unittest
from unittest.mock import patch
from fastapi import HTTPException
from app.services.transcription_service import transcription_service

class TestTranscriptionService(unittest.TestCase):
    
    @patch('app.services.transcription_service.caption_service.get_captions')
    @patch('app.services.transcription_service.TranscriptUtils.save_transcript')
    def test_process_transcript_with_captions(self, mock_save, mock_get_captions):
        mock_get_captions.return_value = [{'text': 'Hello', 'start': 0.0, 'duration': 1.0}]
        mock_save.return_value = '/path/to/transcript.json'
        
        response = transcription_service.process_transcript('vid123', 'video.mp4')
        
        self.assertEqual(response.source_type, 'captions')
        self.assertEqual(response.segment_count, 1)
        mock_save.assert_called_once()
        
    @patch('app.services.transcription_service.caption_service.get_captions')
    @patch('app.services.transcription_service.whisper_service.transcribe')
    @patch('app.services.transcription_service.Path.exists')
    @patch('app.services.transcription_service.TranscriptUtils.save_transcript')
    def test_process_transcript_with_whisper_fallback(self, mock_save, mock_exists, mock_transcribe, mock_get_captions):
        mock_get_captions.return_value = None # Captions fail
        mock_exists.return_value = True # Video file exists
        mock_transcribe.return_value = [{'start': 0.0, 'end': 1.0, 'text': 'Whisper text'}]
        mock_save.return_value = '/path/to/transcript.json'
        
        response = transcription_service.process_transcript('vid123', 'video.mp4')
        
        self.assertEqual(response.source_type, 'whisper')
        self.assertEqual(response.segment_count, 1)
        mock_transcribe.assert_called_once_with('video.mp4', 'vid123')
        
    @patch('app.services.transcription_service.caption_service.get_captions')
    @patch('app.services.transcription_service.Path.exists')
    def test_process_transcript_no_video_file_for_whisper(self, mock_exists, mock_get_captions):
        mock_get_captions.return_value = None # Captions fail
        mock_exists.return_value = False # Video file missing
        
        with self.assertRaises(HTTPException) as context:
            transcription_service.process_transcript('vid123', 'missing.mp4')
            
        self.assertEqual(context.exception.status_code, 404)
