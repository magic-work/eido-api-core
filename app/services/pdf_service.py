from fastapi import  UploadFile
from fastapi_pagination import Params
from fastapi_pagination.ext.beanie import paginate
from app.models.PDFDocument import PDFDocument
from app.services.external.cloudinary_service import CloudinaryService


class PDFService:

    async def get_all_pdfs(self, params: Params):
        return await paginate(PDFDocument, params, sort=["-created_at_utc" ])

    async def create(self, title: str, file: UploadFile):
        pdf_file = CloudinaryService(file.file).upload_pdf()
        pdf_doc = PDFDocument(title=title, pdf=pdf_file)
        return await pdf_doc.create()
