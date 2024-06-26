from app.models.MongoModel import MongoModel
from app.models.Media import PDF


class PDFDocument(MongoModel):
    title: str
    pdf: PDF
