from pydantic import BaseModel
class LoginSchema(BaseModel):
    username: str
    password: str

class LoginResponseSchema(BaseModel):
    token: str

