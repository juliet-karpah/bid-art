import pytest
from fastapi import HTTPException
from app.core.dependencies import require_role
from app.models.user import User

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/auth/register",
        json={
            "name": "TestUser",
            "email": "test@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password_hash" not in data

@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "StrongPassword123!",
    }

    first_response = await client.post("/auth/register", json=user_data)
    second_response = await client.post("/auth/register", json=user_data)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "This user already exists"

@pytest.mark.asyncio
async def test_login_success(client):
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "StrongPassword123!",
    }

    await client.post("/auth/register", json=user_data)

    response = await client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "StrongPassword123!",
        },
    )

    response = await client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    response = await client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

@pytest.mark.asyncio
async def test_get_current_user(client):
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "StrongPassword123!",
    }

    await client.post("/auth/register", json=user_data)

    login_response = await client.post(
        "/auth/login",
        json={
            "email": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]

    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert "password_hash" not in data

@pytest.mark.asyncio
async def test_get_current_user_without_token(client):
    response = await client.get("/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client):
    response = await client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"

@pytest.mark.asyncio
async def test_admin_role_allowed():
    admin = User(
        name="Admin User",
        email="admin@example.com",
        password_hash="test-hash",
        role="admin",
    )

    role_dependency = require_role("admin")

    result = await role_dependency(current_user=admin)

    assert result == admin

@pytest.mark.asyncio
async def test_seller_rejected_from_admin_resource():
    seller = User(
        name="Seller User",
        email="seller@example.com",
        password_hash="test-hash",
        role="seller",
    )

    role_dependency = require_role("admin")

    with pytest.raises(HTTPException) as exc_info:
        await role_dependency(current_user=seller)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You do not have permission"