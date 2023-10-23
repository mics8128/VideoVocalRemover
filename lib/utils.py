import re

def is_youtube_url(url: str) -> bool:
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=[a-zA-Z0-9_-]+|embed/[a-zA-Z0-9_-]+|v/[a-zA-Z0-9_-]+)?'
    )
    
    return re.match(youtube_regex, url) is not None