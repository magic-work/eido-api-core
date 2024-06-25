from app.models.MongoModel import MongoModel, AppBaseModel
from app.models.Media import PDFDocument
from app.logs import get_logger

logger = get_logger(__name__)


class Patient(MongoModel):
    user_id: str
    name: str
    additional_info: str
    pdfs: list[PDFDocument]


class PatientCreate(AppBaseModel):
    name: str
    additional_info: str
    pdfs: list[PDFDocument]


class PatientUpdate(AppBaseModel):
    name: str | None = None
    additional_info: str | None = None
    pdfs: list[PDFDocument] | None = None
