from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from app.settings import get_settings
from app.models.Entity import Entity
from app.logs import get_logger
from app.services.entity_service import EntityService


logger = get_logger(__name__)
settings = get_settings()

router = APIRouter(
    prefix='/entities',
    tags=[''],
)


@router.get('/my-entities', status_code=status.HTTP_200_OK, response_model=Page[Entity])
async def get_my_entities(entity = Depends(EntityService().get_my_entities)):
    return entity


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=Entity)
async def get_entity_by_id(entity: Entity = Depends(EntityService().get_by_id)):
    return entity


@router.post('', status_code=status.HTTP_201_CREATED, response_model=Entity)
async def create_entity(entity: Entity = Depends(EntityService().create)):
    return entity


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=Entity)
async def update_entity(entity: Entity = Depends(EntityService().update)):
    return entity


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(EntityService().delete)])
async def delete_entity() -> None:
    pass
