from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch(
    "app.services.video_ingestion_service."
    "video_ingestion_service.ingest_youtube_video"
)
def test_ingest_youtube_video_success(
    mock_ingestion,
):

    mock_ingestion.return_value = {
        "video": {
            "url": (
                "https://www.youtube.com/"
                "watch?v=dQw4w9WgXcQ"
            ),
            "video_id": "dQw4w9WgXcQ",
            "title": "Test Video",
            "duration": 120,
            "channel": "Test Channel",
            "local_path": (
                "storage/videos/"
                "dQw4w9WgXcQ.mp4"
            ),
        },
        "transcript": {
            "video_id": "dQw4w9WgXcQ",
            "transcript_path": (
                "storage/transcripts/raw/"
                "dQw4w9WgXcQ.json"
            ),
            "source_type": "captions",
            "segment_count": 1,
            "segments": [
                {
                    "start": 0.0,
                    "end": 2.5,
                    "text": "Hello world",
                }
            ],
        },
        "frames": {
            "video_id": "dQw4w9WgXcQ",
            "frame_count": 2,
            "frames": [
                {
                    "timestamp": 0,
                    "frame_path": (
                        "storage/frames/"
                        "dQw4w9WgXcQ/frame_0000.jpg"
                    ),
                },
                {
                    "timestamp": 2,
                    "frame_path": (
                        "storage/frames/"
                        "dQw4w9WgXcQ/frame_0001.jpg"
                    ),
                },
            ],
        },
    }

    response = client.post(
        "/video/youtube",
        json={
            "url": (
                "https://www.youtube.com/"
                "watch?v=dQw4w9WgXcQ"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["video"]["video_id"]
        == "dQw4w9WgXcQ"
    )

    assert (
        data["video"]["title"]
        == "Test Video"
    )

    assert (
        data["transcript"]["source_type"]
        == "captions"
    )

    assert (
        data["transcript"]["segment_count"]
        == 1
    )

    assert (
        data["transcript"]["segments"][0]["text"]
        == "Hello world"
    )

    assert (
        data["frames"]["frame_count"]
        == 2
    )

    assert (
        data["frames"]["frames"][0]
        ["timestamp"]
        == 0
    )

    assert (
        data["frames"]["frames"][0]
        ["frame_path"]
        .endswith(".jpg")
    )


def test_ingest_youtube_video_invalid_url():

    response = client.post(
        "/video/youtube",
        json={
            "url": "https://vimeo.com/123456"
        },
    )

    assert response.status_code == 400

    assert (
        "Invalid YouTube URL"
        in response.json()["detail"]
    )


@patch(
    "app.services.video_ingestion_service."
    "video_ingestion_service.ingest_youtube_video"
)
def test_ingest_youtube_video_too_long(
    mock_ingestion,
):

    mock_ingestion.side_effect = ValueError(
        "Video is too long (500s). "
        "Maximum allowed length is 7 minutes."
    )

    response = client.post(
        "/video/youtube",
        json={
            "url": (
                "https://www.youtube.com/"
                "watch?v=dQw4w9WgXcQ"
            )
        },
    )

    assert response.status_code == 400

    assert (
        "Video is too long"
        in response.json()["detail"]
    )