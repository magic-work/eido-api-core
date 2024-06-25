import pytest
from app.tests.fixtures.sample_entities import entity_teapot, entity_hamburger


@pytest.fixture(scope="function")
async def create_entity_teapot(async_client, login_as_quill):
    response = await async_client.post("/entities", json=entity_teapot)
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
async def create_entity_hamburger(async_client, login_as_rocket):
    response = await async_client.post("/entities", json=entity_hamburger)
    assert response.status_code == 201
    return response.json()


async def test_read_all_entities_as_admin(async_client, login_as_admin, create_entity_teapot, create_entity_hamburger):
    response = await async_client.get("/admin/entities")
    assert response.status_code ==  200
    items = response.json().get('items')
    assert len(items) == 2


async def test_unauthorized_read(async_client):
    response = await async_client.get("/admin/entities")
    assert response.status_code == 403


async def test_refuse_to_return_all_entities_with_bad_token(async_client):
    response = await async_client.get("/admin/entities", headers={"Authorization": "Bearer bad"})
    assert response.status_code == 401


async def test_get_my_entities(async_client, login_as_quill, create_entity_teapot):
    response = await async_client.get("/entities/my-entities")
    assert response.status_code == 200
    items = response.json().get('items')
    assert len(items) == 1
    assert items[0]['name'] == 'Teapot'


async def test_create_entity(async_client, login_as_quill, create_entity_teapot):
    response = create_entity_teapot
    assert response['name'] == 'Teapot'
    assert response['description'] == 'I\'m a little teapot, short and stout'


async def test_get_entity_by_user_id(async_client, login_as_quill, create_entity_teapot):
    response = await async_client.get(f"/entities/{create_entity_teapot['_id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Teapot"
    assert response.json()["description"] == "I'm a little teapot, short and stout"


async def test_get_entity_by_user_id_not_found(async_client, login_as_quill):
    response = await async_client.get("/entities/660194b687cb2dd49f880f28")
    assert response.status_code == 404


async def test_update_my_entity(async_client, login_as_quill, create_entity_teapot):
    response = await async_client.patch(f"/entities/{create_entity_teapot['_id']}", json={
        "name": "I'm a kettle!",
    })
    assert response.status_code == 200
    response = await async_client.get("/entities/my-entities")
    items = response.json().get('items')
    assert len(items) == 1
    assert items[0]["name"] == "I'm a kettle!"
    assert items[0]["description"] == "I'm a little teapot, short and stout"


async def test_cannot_update_another_users_entity(async_client, create_entity_teapot, login_as_rocket):
    response = await async_client.patch(f"/entities/{create_entity_teapot['_id']}", json={
        "name": "My entity",
    })
    assert response.status_code == 403


async def test_delete_my_entity(async_client, login_as_quill, create_entity_teapot):
    response = await async_client.delete(f"/entities/{create_entity_teapot['_id']}")
    assert response.status_code == 204
    response = await async_client.get("/entities/my-entities")
    items = response.json().get('items')
    assert len(items) == 0


async def test_cannot_delete_other_users_entity(async_client, create_entity_teapot, login_as_rocket):
    response = await async_client.delete(f"/entities/{create_entity_teapot['_id']}")
    assert response.status_code == 403
