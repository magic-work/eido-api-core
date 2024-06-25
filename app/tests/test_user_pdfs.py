import pytest
from app.tests.fixtures.sample_user_pdfs import user_pdf_teapot, user_pdf_hamburger


@pytest.fixture(scope="function")
async def create_user_pdf_teapot(async_client, login_as_quill):
    response = await async_client.post("/user_pdfs", json=user_pdf_teapot)
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
async def create_user_pdf_hamburger(async_client, login_as_rocket):
    response = await async_client.post("/user_pdfs", json=user_pdf_hamburger)
    assert response.status_code == 201
    return response.json()


async def test_read_all_entities_as_admin(async_client, login_as_admin, create_user_pdf_teapot, create_user_pdf_hamburger):
    response = await async_client.get("/admin/user_pdfs")
    assert response.status_code ==  200
    items = response.json().get('items')
    assert len(items) == 2


async def test_unauthorized_read(async_client):
    response = await async_client.get("/admin/user_pdfs")
    assert response.status_code == 403


async def test_refuse_to_return_all_entities_with_bad_token(async_client):
    response = await async_client.get("/admin/user_pdfs", headers={"Authorization": "Bearer bad"})
    assert response.status_code == 401


async def test_get_my_entities(async_client, login_as_quill, create_user_pdf_teapot):
    response = await async_client.get("/user_pdfs/my-user_pdfs")
    assert response.status_code == 200
    items = response.json().get('items')
    assert len(items) == 1
    assert items[0]['name'] == 'Teapot'


async def test_create_user_pdf(async_client, login_as_quill, create_user_pdf_teapot):
    response = create_user_pdf_teapot
    assert response['name'] == 'Teapot'
    assert response['description'] == 'I\'m a little teapot, short and stout'


async def test_get_user_pdf_by_user_id(async_client, login_as_quill, create_user_pdf_teapot):
    response = await async_client.get(f"/user_pdfs/{create_user_pdf_teapot['_id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Teapot"
    assert response.json()["description"] == "I'm a little teapot, short and stout"


async def test_get_user_pdf_by_user_id_not_found(async_client, login_as_quill):
    response = await async_client.get("/user_pdfs/660194b687cb2dd49f880f28")
    assert response.status_code == 404


async def test_update_my_user_pdf(async_client, login_as_quill, create_user_pdf_teapot):
    response = await async_client.patch(f"/user_pdfs/{create_user_pdf_teapot['_id']}", json={
        "name": "I'm a kettle!",
    })
    assert response.status_code == 200
    response = await async_client.get("/user_pdfs/my-user_pdfs")
    items = response.json().get('items')
    assert len(items) == 1
    assert items[0]["name"] == "I'm a kettle!"
    assert items[0]["description"] == "I'm a little teapot, short and stout"


async def test_cannot_update_another_users_user_pdf(async_client, create_user_pdf_teapot, login_as_rocket):
    response = await async_client.patch(f"/user_pdfs/{create_user_pdf_teapot['_id']}", json={
        "name": "My user_pdf",
    })
    assert response.status_code == 403


async def test_delete_my_user_pdf(async_client, login_as_quill, create_user_pdf_teapot):
    response = await async_client.delete(f"/user_pdfs/{create_user_pdf_teapot['_id']}")
    assert response.status_code == 204
    response = await async_client.get("/user_pdfs/my-user_pdfs")
    items = response.json().get('items')
    assert len(items) == 0


async def test_cannot_delete_other_users_user_pdf(async_client, create_user_pdf_teapot, login_as_rocket):
    response = await async_client.delete(f"/user_pdfs/{create_user_pdf_teapot['_id']}")
    assert response.status_code == 403
