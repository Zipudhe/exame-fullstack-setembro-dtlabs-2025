from uuid import uuid4
import re

from typing import Annotated
from pydantic import BaseModel, Field, AfterValidator
from fastapi import Form


def check_password_pattern(password: str) -> str:
    regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
    result = re.search(regex, password)

    if result is None:
        raise ValueError(
            "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one number."
        )

    return password


SecurePassword = Annotated[str, AfterValidator(check_password_pattern)]


class UserIn(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    username: str = Field()
    password: SecurePassword = Field()
    model_config = {"extra": "forbid"}


class UserLogin(BaseModel):
    username: str = Field()
    password: str = Field()
    model_config = {"extra": "forbid"}


UserInputForm = Annotated[UserIn, Form()]

UserLoginForm = Annotated[UserLogin, Form()]


class UserOut(BaseModel):
    id: str = Field()
    username: str = Field()


class UserCreated(BaseModel):
    id: str = Field()
