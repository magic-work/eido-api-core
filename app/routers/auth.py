from fastapi import APIRouter, Depends, status
from app.settings import get_settings
from app.logs import get_logger
from app.services.auth import set_user_role

logger = get_logger(__name__)
settings = get_settings()

router = APIRouter(
    prefix='/auth',
    tags=['Admin auth'],
)

@router.post("/set-user-role", dependencies=[Depends(set_user_role)], status_code=status.HTTP_201_CREATED)
async def user_role_setter():
    pass
