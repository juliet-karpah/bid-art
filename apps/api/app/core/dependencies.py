from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_session
from app.models.user import User
from sqlalchemy import select
from app.core.security import decode_access_token
from jwt.exceptions import InvalidTokenError
import uuid

bearer_scheme = HTTPBearer(auto_error=False)

async def get_authenticated_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
                                 db: AsyncSession=Depends(get_session)):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        user_id = decode_access_token(credentials.credentials)
        user_uuid = uuid.UUID(user_id)
    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = await db.scalar(select(User).where(User.id == user_uuid))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user