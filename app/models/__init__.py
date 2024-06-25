###########################################################
#
# Data Access Layer (DAL) - Models
#
# This folder contains database models as Python classes, and other routines
# that facilitate database interactions. The DAL provides a structured way
# to interact with the database, separate from business logic.
#
# Keeping models distinct from business logic ensures a clean separation of
# concerns, making it easier to manage and modify the database schema independently.
#
# In this __init__ module, we define a singleton class that initializes the database.
###########################################################
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.Entity import Entity
from app.settings import get_settings

settings = get_settings()

document_models = [
    Entity
]

async def initialize_mongodb():
    client = AsyncIOMotorClient(f"mongodb://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}?authSource=admin")
    await init_beanie(database=client.mongodb, document_models=document_models)
