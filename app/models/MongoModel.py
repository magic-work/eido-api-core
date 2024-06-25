from datetime import datetime, timezone
from pydantic import Field, BaseModel
from beanie import Document


class MongoModel(Document):
    created_at_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        use_revision: bool = True

    async def save(self, *args, **kwargs):
        self.modified_at_utc = datetime.now(timezone.utc)
        return await super().save(*args, **kwargs)


class AppBaseModel(BaseModel):
    def to_dict(self):
        """Use this in place of pydantic's .model_dump() to avoid issues with PydanticObjectId."""
        return {key: value for key, value in self.__dict__.items() if value is not None}
