import asyncio
from aiohttp import ClientSession

async def main():
    async with ClientSession() as session:
        # response = await session.post('http://127.0.0.1:5000/users/', json={
        #     'name': 'SomeName11',
        #     'password': 'Passwordewr_1',
        # })
        # print(response.status)
        # print(await response.json())

        # response = await session.patch('http://127.0.0.1:5000/users/1/', json={
        #     'name': 'Wooft',
        #     'password': 'Password',
        # })
        # print(response.status)
        # print(await response.json(content_type=None))

        # response = await session.post('http://127.0.0.1:5000/announcement/', json={
        #     'title': 'First',
        #     'description': 'Test',
        #     'owner': 1,
        # })
        # print(await response.json())

        # response = await session.get('http://127.0.0.1:5000/users/1/')
        # print(response.status)
        # print(await response.json())

        # response = await session.get('http://127.0.0.1:5000/announcement/5/')
        # print(response.status)
        # print(await response.json(content_type=None))
        #
        # response = await session.patch('http://127.0.0.1:5000/announcement/8/', json={
        #     'title': 'new_title',
        #     'owner': 1,
        #     'password': 'Password'
        # })
        # print(response.status)
        # print(await response.json())
        #
        response = await session.delete('http://0.0.0.0:8000/announcement/7/', json={
            'title': 'new_title',
            'owner': 1,
            'password': 'Password'
        })
        print(response.status)
        print(await response.json())

asyncio.run(main())