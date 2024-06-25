from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from app.settings import get_settings
from app.models.UserPDF import UserPDF
from app.logs import get_logger
from app.services.user_pdf_service import UserPDFService


logger = get_logger(__name__)
settings = get_settings()

router = APIRouter(
    prefix='/user_pdfs',
    tags=[''],
)


@router.get('/my-user_pdfs', status_code=status.HTTP_200_OK, response_model=Page[UserPDF])
async def get_my_entities(user_pdf = Depends(UserPDFService().get_my_entities)):
    return user_pdf


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserPDF)
async def get_user_pdf_by_id(user_pdf: UserPDF = Depends(UserPDFService().get_by_id)):
    return user_pdf


@router.post('', status_code=status.HTTP_201_CREATED, response_model=UserPDF)
async def create_user_pdf(user_pdf: UserPDF = Depends(UserPDFService().create)):
    return user_pdf


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=UserPDF)
async def update_user_pdf(user_pdf: UserPDF = Depends(UserPDFService().update)):
    return user_pdf


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(UserPDFService().delete)])
async def delete_user_pdf() -> None:
    pass
