from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from app.settings import get_settings
from app.models.UserPDF import UserPDF
from app.logs import get_logger
from app.services.auth import get_admin_user
from app.services.user_pdf_service import UserPDFAdminService


logger = get_logger(__name__)
settings = get_settings()

router = APIRouter(
    prefix='/admin/user_pdfs',
    tags=[''],
    dependencies=[Depends(get_admin_user)]
)


@router.get('', status_code=status.HTTP_200_OK, response_model=Page[UserPDF])
async def get_my_entities(user_pdfs = Depends(UserPDFAdminService().get_all_entities)):
    return user_pdfs
