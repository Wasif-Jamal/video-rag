import re

def validate_youtube_url(url: str) -> bool:
    """
    Validates if a given URL is a supported YouTube URL.
    """
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)'
        r'([a-zA-Z0-9_-]{11})'
    )
    match = re.search(youtube_regex, url)
    return bool(match)
