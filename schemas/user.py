from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class UserSchema(BaseModel):
    name: str
    username: str
    email: str
    password: str = Field(min_length=8)

class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

