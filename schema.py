from pydantic import BaseModel, validator
from pydantic import ValidationError

from db import User
from errors import HttpError
import re

PASSWORD_REGEX = re.compile(
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*_?])"
)

class CreateUser(BaseModel):

    name: str
    password: str

    @validator('password')
    def validate_password(cls, value: str):
        if not re.search(PASSWORD_REGEX, value):
            raise ValueError('Password ist easy')
        if len(value) < 9:
            raise ValueError('Password is too short')
        return value

def validate_create_user(json_data):

    try:
        user_schema = CreateUser(**json_data)
        return user_schema.dict()
    except ValidationError as er:
        raise HttpError(status_code=400, message=er.errors())

