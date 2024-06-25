from fastapi import Depends
from fastapi_pagination import Params
from fastapi_pagination.ext.beanie import paginate
from app.models.Entity import Entity, EntityCreate, EntityUpdate
from app.services.base_service import BaseService, BaseAdminService
from app.services.auth import get_current_user, FirebaseUser


class EntityService(BaseService[Entity, EntityCreate, EntityUpdate]):

    def __init__(self):
        super().__init__(Entity)

    async def get_my_entities(self, params: Params = Depends(), current_user: FirebaseUser = Depends(get_current_user)):
        return await paginate(self.model.find({"user_id": current_user.uid}), params, sort=["-created_at_utc" ])

    async def create(self, data: EntityCreate, current_user: FirebaseUser = Depends(get_current_user)):
        return await super().create(data, current_user)

    async def update(self, id: str, data: EntityUpdate, current_user: FirebaseUser = Depends(get_current_user)):
        return await super().update(id, data, current_user)


class EntityAdminService(BaseAdminService[Entity, EntityCreate, EntityUpdate]):

    def __init__(self):
        super().__init__(Entity)

    async def get_all_entities(self, params: Params = Depends()):
        return await paginate(self.model.find(), params, sort=["-created_at_utc" ])

    async def update(self, id: str, data: EntityUpdate):
        return await super().update(id, data)
