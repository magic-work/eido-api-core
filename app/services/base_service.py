from typing import TypeVar, Generic, Type
from fastapi import HTTPException, status, Depends
from beanie import PydanticObjectId
from app.models.MongoModel import MongoModel, AppBaseModel
from app.services.auth import get_current_user, FirebaseUser
from app.logs import get_logger

logger = get_logger(__name__)

T = TypeVar('T', bound=MongoModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=AppBaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=AppBaseModel)


class BaseService(Generic[T, CreateSchemaType, UpdateSchemaType]):
    """
    This is a base service class that provides CRUD operations for whatever model inherits from it.
    It interacts with the model layer and raises http exceptions where necessary. Some methods,
    such as get_by_id() and delete(), can be used directly. Others will need to be called from a
    more specific service class that inherits from this one, since input data types will need to be
    specified.
    """
    def __init__(self, model: Type[T]):
        self.model = model

    async def get_by_id(self, id: PydanticObjectId) -> T:
        db_document = await self.model.get(id)
        if not db_document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
        return db_document

    async def create(self, data: CreateSchemaType, current_user: FirebaseUser) -> T:
        db_document = self.model(user_id=current_user.uid, **data.to_dict())
        return await db_document.create()

    async def update(self, id: PydanticObjectId, data: UpdateSchemaType, current_user: FirebaseUser) -> T:
        db_document = await self.model.get(id)
        if not db_document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot update: Not found")
        if db_document.user_id != current_user.uid:
            logger.warning(f"An attempt was made to modify a record not owned by the current user. User: {current_user.uid}, Record: {db_document.id}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="An attempt was made to modify a record not owned by the current user.")
        return await db_document.update({"$set": data.to_dict()})

    async def delete(self, id: PydanticObjectId, current_user: FirebaseUser = Depends(get_current_user)) -> None:
        db_document = await self.model.get(id)
        if not db_document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot delete: Not found")
        if db_document.user_id != current_user.uid:
            logger.warning(f"An attempt was made to delete a record not owned by the current user. User: {current_user.uid}, Record: {db_document.id}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="An attempt was made to delete a record not owned by the current user.")
        await db_document.delete()


class BaseAdminService(Generic[T, CreateSchemaType, UpdateSchemaType]):
    """
    This is a base service class for handling admin operations. The validation of an
    admin user will happen at the router level, so use this class with care and be sure
    that the admin validation has already been applied.
    """
    def __init__(self, model: Type[T]):
        self.model = model

    async def get_all(self) -> list[T]:
        return await self.model.find().to_list()

    async def get_by_id(self, id: PydanticObjectId) -> T:
        db_document = await self.model.get(id)
        if not db_document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
        return db_document

    async def update(self, id: PydanticObjectId, data: UpdateSchemaType, ) -> T:
        db_document = await self.model.get(id)
        if not db_document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="[Admin] Cannot update record: Not found")
        return await db_document.update({"$set": data.to_dict()})

    async def delete(self, id: PydanticObjectId) -> None:
        db_document = await self.model.get(id)
        if not db_document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="[Admin] Cannot delete record: Not found")
        await db_document.delete()
