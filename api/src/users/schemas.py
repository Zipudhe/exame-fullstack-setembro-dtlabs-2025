from datetime import date
from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str
    created_at: date
    updated_at: date


class UserOut(BaseModel):
    id: str
    username: str
