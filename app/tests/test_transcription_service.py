import json
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from app.services.transcription_service import (
    transcription_service,
)


class TestTranscriptionService(
    unittest.TestCase
):

    @patch(
        "app.services.transcription_service."
        "caption_service.get_captions"
    )
    @patch(
        "app.services.transcription_service."
        "Path.exists"
    )
    @patch(
        "builtins.open",
        new_callable=mock_open,
    )
    def test_process_transcript_with_captions(
        self,
        mock_file,
        mock_exists,
        mock_get_captions,
    ):

        mock_exists.side_effect = [
            False,  # transcript cache missing
            True,   # video file exists
        ]

        mock_get_captions.return_value = [
            {
                "text": "Hello",
                "start": 0.0,
                "duration": 1.0,
            }
        ]

        response = (
            transcription_service
            .process_transcript(
                "vid123",
                "video.mp4",
            )
        )

        self.assertEqual(
            response.source_type,
            "captions",
        )

        self.assertEqual(
            response.segment_count,
            1,
        )

        self.assertEqual(
            response.segments[0].text,
            "Hello",
        )

        mock_get_captions.assert_called_once_with(
            "vid123"
        )

        mock_file.assert_called()


    @patch(
        "app.services.transcription_service."
        "caption_service.get_captions"
    )
    @patch(
        "app.services.transcription_service."
        "whisper_service.transcribe"
    )
    @patch(
        "app.services.transcription_service."
        "Path.exists"
    )
    @patch(
        "builtins.open",
        new_callable=mock_open,
    )
    def test_process_transcript_with_whisper_fallback(
        self,
        mock_file,
        mock_exists,
        mock_transcribe,
        mock_get_captions,
    ):

        mock_exists.side_effect = [
            False,  # transcript cache missing
            True,   # video file exists
        ]

        # captions unavailable
        mock_get_captions.return_value = None

        mock_transcribe.return_value = [
            {
                "start": 0.0,
                "end": 1.0,
                "text": "Whisper text",
            }
        ]

        response = (
            transcription_service
            .process_transcript(
                "vid123",
                "video.mp4",
            )
        )

        self.assertEqual(
            response.source_type,
            "whisper",
        )

        self.assertEqual(
            response.segment_count,
            1,
        )

        self.assertEqual(
            response.segments[0].text,
            "Whisper text",
        )

        mock_transcribe.assert_called_once_with(
            "video.mp4",
            "vid123",
        )


    @patch(
        "app.services.transcription_service."
        "Path.exists"
    )
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps(
            [
                {
                    "start": 0.0,
                    "end": 1.0,
                    "text": "Cached text",
                }
            ]
        ),
    )
    def test_process_transcript_uses_cache(
        self,
        mock_file,
        mock_exists,
    ):

        # cached transcript exists
        mock_exists.return_value = True

        response = (
            transcription_service
            .process_transcript(
                "vid123",
                "video.mp4",
            )
        )

        self.assertEqual(
            response.source_type,
            "cached",
        )

        self.assertEqual(
            response.segment_count,
            1,
        )

        self.assertEqual(
            response.segments[0].text,
            "Cached text",
        )

        mock_file.assert_called_once()