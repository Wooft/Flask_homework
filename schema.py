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

class Announcement(BaseModel):
    title: str
    owner: int


class Owner(BaseModel):
    owner: int
    password: str

async def validate_announcement(json_data):
    try:
        an_shema=Announcement(**json_data)
        return an_shema
    except pydantic.error_wrappers.ValidationError:
        raise web.HTTPBadRequest(text=json.dumps({'error': 'All required fields must be filled'}), content_type='application/json')

async def validate_create_user(json_data):
    try:
        user_schema = User(**json_data)
        return user_schema.dict()
    except pydantic.error_wrappers.ValidationError:
        raise web.HTTPBadRequest(text=json.dumps({'error':'input data incorrect'}), content_type='application/json')

async def validate_owner(json_data):
    try:
        owner_schema = Owner(**json_data)
        return owner_schema
    except pydantic.error_wrappers.ValidationError:
        raise web.HTTPBadRequest(text=json.dumps({'error': 'need authorisation information'}), content_type='application/json')
