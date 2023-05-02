import json
from aiohttp import web
from sqlalchemy.exc import IntegrityError
from bcrypt import hashpw, gensalt, checkpw
from schema import validate_create_user

from db import Session, User, Announcement, engine, Base

app = web.Application()

async def get_user(user_id: int, session: Session):
    user = await session.get(User, user_id)
    if user is None:
        raise web.HTTPNotFound(text=json.dumps({'status': 'error', 'message': 'user not found'}),
                               content_type='application/json')
    return user

#функция получкния объявления
async def get_an(an_id: int, session: Session):
    announcement = await session.get(Announcement, an_id)
    print(announcement)
    if announcement is None:
        raise web.HTTPNotFound(text=json.dumps({
            'status': 'error',
            'message': 'announcement not found'
        }),
        content_type='application/json')

async def get_announcement(an_id: int, session: Session):
    announcement = await session.get(Announcement, an_id)
    if announcement is None:
        raise web.HTTPNotFound(text=json.dumps({'status': 'error', 'message': 'Объявление не найдено'}),
                               content_type='application/json')
    return announcement

async def is_owner(user_id: int, password: str, session: Session):
    user = await session.get(User, user_id)
    if checkpw(password.encode(), user.password.encode()):
        return True
    else:
        raise web.HTTPForbidden(text=json.dumps({'status': 'error',
                                                    'message': 'incorrect authorization data'}),
                                   content_type='application/json')

async def orm_context(app: web.Application):
    print('START')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print('SHUTDOWN')
@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request['session'] = session
        return await handler(request)

app.middlewares.append(session_middleware)

class UserView(web.View):
    async def get(self):
        session = self.request['session']
        user_id = int(self.request.match_info['user_id'])
        user = await get_user(user_id, session)
        return web.json_response({
            'id': user.id,
            'name': user.name,
        })

    async def post(self):
        session = self.request['session']
        json_data = await self.request.json()
        #Проверка корректности воода данных
        await validate_create_user(json_data)
        #Хэширование пароля
        json_data['password'] = hashpw(json_data['password'].encode(), salt=gensalt()).decode()
        user = User(**json_data)
        session.add(user)
        try:
            await session.commit()
        #Ошибка, выбрасываемая когда добавляемый пользователь уже есть в базе
        except IntegrityError as er:
            raise web.HTTPConflict(text=json.dumps({
                'Status':'error',
                'message':'User already Exist'
            }), content_type='application/json')
        return web.json_response({
            'id': user.id,
            'name': user.name,
        })
    async def patch(self):
        user_id = int(self.request.match_info['user_id'])
        user = await get_user(user_id, self.request['session'])
        json_data = await self.request.json()
        #если в данных запроса есть пароль - хэшируем его
        if 'password' in json_data:
            json_data['password'] = hashpw(json_data['password'].encode(), salt=gensalt()).decode()
        for field, values in json_data.items():
            setattr(user, field, values)
        self.request['session'].add(user)
        await self.request['session'].commit()
        print('Готово')
        return web.json_response({
            'status': 'ok'
        })

    async def delete(self):
        pass


class AnView(web.View):
    async def get(self):
        session = self.request['session']
        an_id = int(self.request.match_info['an_id'])
        announcement = await get_announcement(an_id, session)
        print(announcement.title)
        return web.json_response({
            'title': announcement.title,
            'description': announcement.description,
            'time': announcement.creation_time.isoformat()
        })

    async def post(self):
        session = self.request['session']
        json_data = await self.request.json()
        print(json_data)
        announcement = Announcement(**json_data)
        session.add(announcement)
        try:
            await session.commit()
        # Ошибка, выбрасываемая когда добавляемый пользователь уже есть в базе
        except IntegrityError as er:
            raise web.HTTPConflict(text=json.dumps({
                'Status': 'error',
                'message': 'User already Exist'
            }), content_type='application/json')
        return web.json_response({
            'id': announcement.id,
            'title': announcement.title,
            'status': 'created'
        })

    async def patch(self):
        an_id = int(self.request.match_info['an_id'])
        print(f"Жопа: {self.request.match_info['password']}")
        json_data = await self.request.json()
        user = await get_user(json_data['owner'], self.request['session'])
        announcement = await get_announcement(an_id, self.request['session'])
        if await is_owner(json_data['owner'], json_data['password'],self.request['session']):
            for field, values in json_data.items():
                setattr(announcement, field, values)
            self.request['session'].add(user)
            await self.request['session'].commit()
            return web.json_response({
                'status': 'ok'
            })


    async def delete(self):
        an_id = int(self.request.match_info['an_id'])
        json_data = await self.request.json()
        announcement = await get_announcement(an_id, self.request['session'])
        if await is_owner(json_data['owner'], json_data['password'], self.request['session']):
            await self.request['session'].delete(announcement)
            await self.request['session'].commit()
            return web.json_response({
                'messahge': 'Announcement has been removed'
            })


app.cleanup_ctx.append(orm_context)

app.add_routes([
    web.get('/users/{user_id:\d+}/', UserView)
])

app.add_routes([
    web.post('/users/', UserView)
])

app.add_routes([
    web.patch('/users/{user_id:\d+}/', UserView)
])

app.add_routes([
    web.delete('/users/{user_id:\d+}/', UserView)
])

app.add_routes([
    web.get('/announcement/{an_id:\d+}/', AnView)
])

app.add_routes([
    web.post('/announcement/', AnView)
])

app.add_routes([
    web.patch('/announcement/{an_id:\d+}/', AnView)
])

app.add_routes([
    web.delete('/announcement/{an_id:\d+}/', AnView)
])

if __name__ == '__main__':
    web.run_app(app)