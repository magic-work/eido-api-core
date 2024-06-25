from pathlib import Path
import cloudinary
import cloudinary.api
from cloudinary.exceptions import Error
from cloudinary.uploader import upload as cloudinary_upload
from cloudinary.utils import cloudinary_url
from fastapi import HTTPException, status
from app.logs import get_logger
from app.settings import get_settings
from app.models.Media import Image, Video, PDFDocument
logger = get_logger(__name__)
settings = get_settings()

cloudinary.config(
    cloud_name = settings.cloudinary_cloud_name,
    api_key = settings.cloudinary_api_key,
    api_secret = settings.cloudinary_api_secret,
    secure = True
)


class CloudinaryService:

    def __init__(self, file):
        self.file = file

    def upload_media(self) -> None:
        try:
            return self._upload_image()
        except Error:
            try:
                return self._upload_video()
            except Exception as e:
                logger.error("Unable to upload media: %s", e)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"There was a problem uploading the media: {e}")
        except Exception as e:
            logger.error("Unable to upload media: %s", e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There was a problem uploading the media: {e}")

    def upload_pdf_to_cloudinary(self) -> None:
        return self._upload_pdf()

    def _upload_image(self) -> None:
        response = cloudinary_upload(self.file, folder=settings.cloudinary_folder)
        if not response.get('public_id'):
            logger.error("Unable to upload user image: %s", str(response))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to upload image (no public id)")
        public_id = response.get('public_id')
        url, _ = cloudinary_url(public_id)
        return Image(
            media_type='image',
            public_id=public_id,
            public_url=url,
            display_url=self._get_display_url(public_id),
            thumbnail_url=self._get_thumbnail_url(public_id)
        )

    def _upload_video(self) -> None:
        if hasattr(self.file, 'seek'):
            self.file.seek(0)
        response = cloudinary_upload(self.file, resource_type='video', folder=settings.cloudinary_folder)
        if not response.get('public_id'):
            logger.error("Unable to upload user image: %s", str(response))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to upload video (no public id)")
        url = response.get('secure_url')
        return Video(
            media_type='video',
            public_id=response.get('public_id'),
            public_url=url.replace('/video/upload/', '/video/upload/e_volume:mute/'),
            hls_playback_url=response.get('playback_url').replace('/video/upload/', '/video/upload/e_volume:mute/'),
            created_at=response.get('created_at'),
            thumbnail_url=self._get_video_thumbnail(url)
        )

    def _upload_pdf(self) -> None:
        response = cloudinary_upload(self.file, resource_type='raw', folder=settings.cloudinary_folder)
        if not response.get('public_id'):
            logger.error("Unable to upload pdf: %s", str(response))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to upload pdf (no public id)")
        public_id = response.get('public_id')
        url, _ = cloudinary_url(public_id)
        return PDFDocument(
            media_type='pdf',
            public_url= cloudinary_url(url),
            public_id=response.get('public_id'),
        )

    def _get_video_thumbnail(self, url) -> str:
        path = Path(url)
        return str(path.with_suffix('.jpg'))

    def _get_display_url(self, public_id) -> str:
        url, _ = cloudinary_url(public_id, gravity="center", width=900, crop="scale")
        return url

    def _get_thumbnail_url(self, public_id) -> str:
        url, _ = cloudinary_url(public_id, gravity="center", height=350, width=350, crop="thumb")
        return url
