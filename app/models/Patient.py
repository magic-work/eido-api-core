from app.models.MongoModel import MongoModel, AppBaseModel
from app.models.Media import PDF


class Patient(MongoModel):
    user_id: str
    name: str
    additional_info: str
    pdfs: list[PDF]


class PatientCreate(AppBaseModel):
    name: str
    additional_info: str
    pdfs: list[PDF]


class PatientUpdate(AppBaseModel):
    name: str | None = None
    additional_info: str | None = None
    pdfs: list[PDF] | None = None
