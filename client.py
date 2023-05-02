import asyncio
from aiohttp import ClientSession

async def main():
    async with ClientSession() as session:
        # response = await session.post('http://0.0.0.0:8080/users/', json={
        #     'name': 'SomeName11',
        #     'password': 'Passwordewr_1',
        # })
        # print(response.status)
        # print(await response.json())

        # response = await session.patch('http://0.0.0.0:8080/users/1/', json={
        #     'name': 'Wooft',
        #     'password': 'Password',
        # })
        # print(response.status)
        # print(await response.json(content_type=None))

        # response = await session.post('http://0.0.0.0:8080/announcement/', json={
        #     'title': 'First',
        #     'description': 'Test',
        #     'owner': 1,
        # })
        # print(await response.json())

        # response = await session.get('http://0.0.0.0:8080/users/1/')
        # print(response.status)
        # print(await response.json())

        # response = await session.get('http://0.0.0.0:8080/announcement/5/')
        # print(response.status)
        # print(await response.json(content_type=None))
        #
        response = await session.patch('http://0.0.0.0:8080/announcement/8/', json={
            'title': 'new_title',
            'owner': 1,
            'password': 'Password'
        })
        print(response.status)
        print(await response.json())
        #
        # response = await session.delete('http://0.0.0.0:8080/announcement/6/', json={
        #     'title': 'new_title',
        #     'owner': 1,
        #     'password': 'Password'
        # })
        # print(response.status)
        # print(await response.json())

asyncio.run(main())

# import requests
#
# # response = requests.post('http://127.0.0.1:5000/users',
# #                          json={'name': 'Wooft', 'password': 'Wvmrmnk2@fd'})
#
# # response = requests.get('http://127.0.0.1:5000/users/1')
#
# # response = requests.patch('http://127.0.0.1:5000/users/1',
# #                          json={'password': '1234'})
#
# # response = requests.delete('http://127.0.0.1:5000/users/3')
# #
# response = requests.post('http://127.0.0.1:5000/announcment',
#                          json={
#                              'title': 'Второй заголовок',
#                              'description': 'Какое-то описание',
#                              'owner': 1,
#                              'password': '1234'
#                          })
#
# # response = requests.get('http://127.0.0.1:5000/announcment/2')
#
# # response = requests.patch('http://127.0.0.1:5000/announcment/1',
# #                          json={
# #                              'title': 'Новый заголовок',
# #                              'description': 'Какое-то описание',
# #                              'password': '1234'
# #                          })
# # response = requests.delete('http://127.0.0.1:5000/announcment/2',
# #                          json={
# #                              'owner': 1,
# #                              'password': '1234'
# #                          })
#
# print(response.status_code)
# print(response.json())