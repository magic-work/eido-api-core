import pytest
from beanie import init_beanie
from httpx import AsyncClient
from mongomock_motor import AsyncMongoMockClient
from app.models import document_models
from app.main import app
from app.services.auth import get_current_user, get_admin_user
from app.tests.fixtures.sample_users import admin, quill, rocket


@pytest.fixture(scope="function")
async def mock_mongodb():
    client = AsyncMongoMockClient()
    await init_beanie(database=client.mongodb, document_models=document_models)


@pytest.fixture(scope="function")
async def async_client(mock_mongodb):
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(scope="function")
async def login_as_quill():
    app.dependency_overrides[get_current_user] = lambda: quill
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def login_as_rocket():
    app.dependency_overrides[get_current_user] = lambda: rocket
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def login_as_admin():
    app.dependency_overrides[get_admin_user] = lambda: admin
    yield
    app.dependency_overrides.clear()
