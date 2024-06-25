from app.models.MongoModel import MongoModel, AppBaseModel
from app.logs import get_logger

logger = get_logger(__name__)


class UserPDF(MongoModel):
    user_id: str
    name: str
    description: str


class UserPDFCreate(AppBaseModel):
    name: str
    description: str


class UserPDFUpdate(AppBaseModel):
    name: str | None = None
    description: str | None = None
