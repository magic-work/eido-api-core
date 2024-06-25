from app.models.MongoModel import MongoModel, AppBaseModel
from app.logs import get_logger

logger = get_logger(__name__)


class Entity(MongoModel):
    user_id: str
    name: str
    description: str


class EntityCreate(AppBaseModel):
    name: str
    description: str


class EntityUpdate(AppBaseModel):
    name: str | None = None
    description: str | None = None
