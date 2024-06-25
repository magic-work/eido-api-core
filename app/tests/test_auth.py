from app.tests.fixtures.sample_users import quill


async def test_set_user_role(async_client, mocker, login_as_admin):
    mock_set_custom_user_claims = mocker.patch('app.services.auth.auth.set_custom_user_claims')
    response = await async_client.post("/auth/set-user-role", json={"uid": "iamquill", "role": "admin"})
    mock_set_custom_user_claims.assert_called_once_with('iamquill', {'role': "admin"})
    assert response.status_code == 201


async def test_set_user_role_unauthorized(async_client, mocker):
    mocker.patch('app.services.auth.auth.set_custom_user_claims')
    mocker.patch('app.services.auth.get_current_user', return_value=quill)
    response = await async_client.post(
        "/auth/set-user-role",
        headers={"Authorization": "Bearer invalid_token"},
        json={"uid": "iamquill", "role": "admin"}
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'You are not an admin.'}


async def test_set_user_role_missing_token(async_client):
    response = await async_client.post("/auth/set-user-role")
    assert response.status_code == 403
