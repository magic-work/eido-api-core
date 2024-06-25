from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from app.settings import get_settings
from app.models.Entity import Entity
from app.logs import get_logger
from app.services.auth import get_admin_user
from app.services.entity_service import EntityAdminService


logger = get_logger(__name__)
settings = get_settings()

router = APIRouter(
    prefix='/admin/entities',
    tags=[''],
    dependencies=[Depends(get_admin_user)]
)


@router.get('', status_code=status.HTTP_200_OK, response_model=Page[Entity])
async def get_my_entities(entities = Depends(EntityAdminService().get_all_entities)):
    return entities
