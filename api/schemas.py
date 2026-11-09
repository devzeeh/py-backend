from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

# Input Schemas (Clients send us)
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

# Output Schema (Send back to client safely)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True) # Allow pydantic to read data directly from SQLAlchemy model instances

class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool
    user_id: int

    model_config = ConfigDict(from_attributes=True)