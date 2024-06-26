from fastapi import APIRouter, Depends, status, File, UploadFile
from fastapi_pagination import Params, Page
from app.settings import get_settings
from app.logs import get_logger
from app.models.PDFDocument import PDFDocument
from app.services.pdf_service import PDFService
from app.services.auth import get_current_user

logger = get_logger(__name__)
settings = get_settings()

router = APIRouter(
    prefix='/pdf',
    tags=['PDF documents'],
    # dependencies=[Depends(get_current_user)],
)


@router.get('', status_code=status.HTTP_200_OK, response_model=Page[PDFDocument])
async def get_pdfs(params: Params = Depends()):
    return await PDFService().get_all_pdfs(params)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_pdf(title: str = File(...), pdf_file: UploadFile = File(...)) -> None:
    await PDFService().create(title, pdf_file)
