from fastapi import Depends
from fastapi_pagination import Params
from fastapi_pagination.ext.beanie import paginate
from app.models.Patient import Patient, PatientCreate, PatientUpdate
from app.services.base_service import BaseService, BaseAdminService
from app.services.auth import get_current_user, FirebaseUser


class PatientService(BaseService[Patient, PatientCreate, PatientUpdate]):

    def __init__(self):
        super().__init__(Patient)

    async def get_my_patients(self, params: Params = Depends(), current_user: FirebaseUser = Depends(get_current_user)):
        return await paginate(self.model.find({"user_id": current_user.uid}), params, sort=["-created_at_utc" ])

    async def create(self, data: PatientCreate, current_user: FirebaseUser = Depends(get_current_user)):
        return await super().create(data, current_user)

    async def update(self, id: str, data: PatientUpdate, current_user: FirebaseUser = Depends(get_current_user)):
        return await super().update(id, data, current_user)


class PatientAdminService(BaseAdminService[Patient, PatientCreate, PatientUpdate]):

    def __init__(self):
        super().__init__(Patient)

    async def get_all_patients(self, params: Params = Depends()):
        return await paginate(self.model.find(), params, sort=["-created_at_utc" ])

    async def update(self, id: str, data: PatientUpdate):
        return await super().update(id, data)
