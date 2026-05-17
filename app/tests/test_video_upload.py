from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

@patch('app.routes.video_upload.youtube_service.get_metadata')
@patch('app.routes.video_upload.video_download_service.download_video')
def test_upload_youtube_video_success(mock_download, mock_metadata):
    mock_metadata.return_value = {
        'id': 'dQw4w9WgXcQ',
        'title': 'Test Video',
        'duration': 120,
        'channel': 'Test Channel'
    }
    mock_download.return_value = '/absolute/path/to/storage/videos/dQw4w9WgXcQ.mp4'
    
    response = client.post(
        "/video/youtube",
        json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["video_id"] == "dQw4w9WgXcQ"
    assert data["title"] == "Test Video"
    assert data["duration"] == 120
    assert data["local_path"] == "/absolute/path/to/storage/videos/dQw4w9WgXcQ.mp4"

def test_upload_youtube_video_invalid_url():
    response = client.post(
        "/video/youtube",
        json={"url": "https://vimeo.com/123456"}
    )
    
    assert response.status_code == 400
    assert "Invalid YouTube URL" in response.json()["detail"]

@patch('app.routes.video_upload.youtube_service.get_metadata')
def test_upload_youtube_video_too_long(mock_metadata):
    mock_metadata.return_value = {
        'id': 'dQw4w9WgXcQ',
        'title': 'Test Video',
        'duration': 500, # 400 seconds is > 7 minutes
        'channel': 'Test Channel'
    }
    
    response = client.post(
        "/video/youtube",
        json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
    )
    
    assert response.status_code == 400
    assert "Video is too long" in response.json()["detail"]
