from pydantic import BaseModel, EmailStr, Field, ConfigDict
import uuid

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class RegisterModel(LoginModel):
    name: str=Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=128)

class CurrentUserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    email: EmailStr


