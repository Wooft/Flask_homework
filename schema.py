import json
import pydantic.error_wrappers
from pydantic import BaseModel, validator
from aiohttp import web
import re

PASSWORD_REGEX = re.compile(
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*_?])"
)

class User(BaseModel):
    name: str
    password: str

    @validator('password')
    def validate_password(cls, value):
        if not re.search(PASSWORD_REGEX, value):
            raise web.HTTPBadRequest(text=json.dumps({'error': 'password is too easy'}), content_type='application/json')
        if len(value) < 9:
            raise web.HTTPBadRequest(text=json.dumps({'error': 'password is too short'}), content_type='application/json')


async def validate_create_user(json_data):
    try:
        user_schema = User(**json_data)
        return user_schema.dict()
    except pydantic.error_wrappers.ValidationError as er:
        raise web.HTTPBadRequest(text=json.dumps({'error':'input data incorrect'}), content_type='application/json')
