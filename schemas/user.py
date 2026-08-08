from datetime import datetime
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: str
    username: str
    email: str
    password: str = Field(min_length=8)

class UserResponseSchema(BaseModel):
    name: str
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

