from pydantic import BaseModel
from app.models.MongoModel import MongoModel
from app.settings import get_settings

settings = get_settings()


class Notification(BaseModel):
    title: str
    body: str
    image_url: str | None = None
    deep_link_url: str | None = None


class UserNotification(MongoModel):
    user_id: str
    notification: Notification
    is_read: bool = False



class UserNotificationPreferences(MongoModel):
    user_id: str
    # Add entity specific notification preferences here

    @classmethod
    async def user_preferences(cls, user_id: str) -> "UserNotificationPreferences":
        user_preferences = await cls.find_one({"user_id": user_id})
        if not user_preferences:
            user_preferences = await cls(user_id=user_id).create()
        return user_preferences


class UserNotificationPreferencesUpdate(BaseModel):
    # Add entity specific notification preferences here
    ...
