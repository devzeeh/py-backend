from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegisterShema(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    done: Optional[bool] = None