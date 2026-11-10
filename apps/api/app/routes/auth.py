from fastapi import APIRouter, status, Depends, HTTPException
from app.db.base import get_session
from app.schemas.auth import RegisterModel, LoginModel, CurrentUserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_authenticated_user, require_role


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: RegisterModel, db: AsyncSession = Depends(get_session)):
    user = await db.scalar(select(User).where(User.email == data.email))
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This user already exists")

    new_user = User(
        name= data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}
    

@router.post("/login")
async def login(data: LoginModel, db: AsyncSession = Depends(get_session)):
    user = await db.scalar(select(User).where(User.email == data.email))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token(str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=CurrentUserModel)
async def get_current_user(user: User = Depends(get_authenticated_user)):
    return user

