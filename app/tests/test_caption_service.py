import unittest
from unittest.mock import patch
from app.services.caption_service import caption_service
from youtube_transcript_api import TranscriptsDisabled

class DummySnippet:
    def __init__(self, text, start, duration):
        self.text = text
        self.start = start
        self.duration = duration

class TestCaptionService(unittest.TestCase):
    @patch('app.services.caption_service.YouTubeTranscriptApi.fetch')
    def test_get_captions_success(self, mock_fetch):
        mock_data = [DummySnippet('Hello', 0.0, 1.0)]
        mock_fetch.return_value = mock_data
        
        result = caption_service.get_captions('video_id')
        self.assertEqual(result, [{'text': 'Hello', 'start': 0.0, 'duration': 1.0}])

    @patch('app.services.caption_service.YouTubeTranscriptApi.fetch')
    def test_get_captions_disabled(self, mock_fetch):
        mock_fetch.side_effect = TranscriptsDisabled('video_id')
        
        result = caption_service.get_captions('video_id')
        self.assertIsNone(result)
