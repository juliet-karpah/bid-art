from pydantic import BaseModel, EmailStr, Field
import uuid

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class RegisterModel(LoginModel):
    name: str=Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=128)

class CurrentUserModel(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr


