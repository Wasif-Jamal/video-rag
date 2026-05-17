import unittest
from unittest.mock import patch, MagicMock
from app.services.youtube_service import youtube_service
from app.utils.youtube_validators import validate_youtube_url

class TestYouTubeValidators(unittest.TestCase):
    def test_validate_youtube_url_valid(self):
        self.assertTrue(validate_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
        self.assertTrue(validate_youtube_url("https://youtu.be/dQw4w9WgXcQ"))
        self.assertTrue(validate_youtube_url("https://youtube.com/embed/dQw4w9WgXcQ"))

    def test_validate_youtube_url_invalid(self):
        self.assertFalse(validate_youtube_url("https://vimeo.com/123456"))
        self.assertFalse(validate_youtube_url("https://www.youtube.com/watch?v=123"))
        self.assertFalse(validate_youtube_url("not a url"))

class TestYouTubeService(unittest.TestCase):
    @patch('app.services.youtube_service.yt_dlp.YoutubeDL')
    def test_get_metadata(self, mock_ytdl):
        mock_instance = MagicMock()
        mock_ytdl.return_value.__enter__.return_value = mock_instance
        mock_instance.extract_info.return_value = {
            'id': 'dQw4w9WgXcQ',
            'title': 'Never Gonna Give You Up',
            'duration': 212,
            'uploader': 'RickAstleyVEVO'
        }
        
        metadata = youtube_service.get_metadata("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        self.assertEqual(metadata['id'], 'dQw4w9WgXcQ')
        self.assertEqual(metadata['title'], 'Never Gonna Give You Up')
        self.assertEqual(metadata['duration'], 212)
        self.assertEqual(metadata['channel'], 'RickAstleyVEVO')
