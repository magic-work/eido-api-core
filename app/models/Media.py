"""
We use an abstract base class for Image/Video handling since we'll have
different services (cloudinary and bunny at present) for handling media,
but they must be consumed on the client in a consistent format.
"""
from abc import ABC
from pydantic import BaseModel


class Media(BaseModel, ABC):
    public_url: str


class Image(Media):
    public_id: str
    thumbnail_url: str
    display_url: str
    media_type: str = 'image'


class Video(Media):
    public_id: str
    hls_playback_url: str
    thumbnail_url: str
    created_at: str
    media_type: str = 'video'
