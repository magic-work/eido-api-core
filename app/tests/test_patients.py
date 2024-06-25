import pytest
from app.tests.fixtures.sample_patients import patient_teapot


@pytest.fixture(scope="function")
async def create_patient_teapot(async_client, login_as_quill):
    response = await async_client.post("/patients", json=patient_teapot)
    assert response.status_code == 201
    return response.json()


async def test_get_my_patients(async_client, login_as_quill, create_patient_teapot):
    response = await async_client.get("/patients/my-patients")
    assert response.status_code == 200
    items = response.json().get('items')
    assert len(items) == 1
    assert items[0]['name'] == 'Mary Smith'


async def test_create_patient(async_client, login_as_quill, create_patient_teapot):
    response = create_patient_teapot
    assert response['name'] == 'Mary Smith'
    assert response['additional_info'] == 'I\'m a little teapot, short and stout'


async def test_get_patient_by_user_id(async_client, login_as_quill, create_patient_teapot):
    response = await async_client.get(f"/patients/{create_patient_teapot['_id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Mary Smith"
    assert response.json()["additional_info"] == "I'm a little teapot, short and stout"


async def test_get_patient_by_user_id_not_found(async_client, login_as_quill):
    response = await async_client.get("/patients/660194b687cb2dd49f880f28")
    assert response.status_code == 404


async def test_update_my_patient(async_client, login_as_quill, create_patient_teapot):
    response = await async_client.patch(f"/patients/{create_patient_teapot['_id']}", json={
        "name": "I'm a kettle!",
    })
    assert response.status_code == 200
    response = await async_client.get("/patients/my-patients")
    items = response.json().get('items')
    assert len(items) == 1
    assert items[0]["name"] == "I'm a kettle!"
    assert items[0]["additional_info"] == "I'm a little teapot, short and stout"


async def test_cannot_update_another_users_patient(async_client, create_patient_teapot, login_as_rocket):
    response = await async_client.patch(f"/patients/{create_patient_teapot['_id']}", json={
        "name": "My patient",
    })
    assert response.status_code == 403


async def test_delete_my_patient(async_client, login_as_quill, create_patient_teapot):
    response = await async_client.delete(f"/patients/{create_patient_teapot['_id']}")
    assert response.status_code == 204
    response = await async_client.get("/patients/my-patients")
    items = response.json().get('items')
    assert len(items) == 0


async def test_cannot_delete_other_users_patient(async_client, create_patient_teapot, login_as_rocket):
    response = await async_client.delete(f"/patients/{create_patient_teapot['_id']}")
    assert response.status_code == 403
