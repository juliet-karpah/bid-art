import pytest
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


def test_hash_password():
    password = "StrongPassword123!"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert isinstance(hashed_password, str)


def test_verify_password_success():
    password = "StrongPassword123!"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_failure():
    password = "StrongPassword123!"
    hashed_password = hash_password(password)

    assert verify_password("WrongPassword123!", hashed_password) is False


def test_create_and_decode_access_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY",  "test-secret-key-that-is-at-least-32-bytes-long")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")

    user_id = "test-user-id"

    token = create_access_token(user_id)
    decoded_user_id = decode_access_token(token)

    assert decoded_user_id == user_id


def test_decode_expired_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY",  "test-secret-key-that-is-at-least-32-bytes-long")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")

    expired_payload = {
        "sub": "test-user-id",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
    }

    token = jwt.encode(
        expired_payload,
         "test-secret-key-that-is-at-least-32-bytes-long",
        algorithm="HS256",
    )

    with pytest.raises(InvalidTokenError):
        decode_access_token(token)


def test_decode_token_without_sub(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY",  "test-secret-key-that-is-at-least-32-bytes-long")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")

    token = jwt.encode(
        {"exp": datetime.now(timezone.utc) + timedelta(minutes=30)},
         "test-secret-key-that-is-at-least-32-bytes-long",
        algorithm="HS256",
    )

    with pytest.raises(InvalidTokenError):
        decode_access_token(token)