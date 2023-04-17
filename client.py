import requests

# response = requests.post('http://127.0.0.1:5000/users',
#                          json={'name': 'Wooft', 'password': 'Wvmrmnk2@fd'})

# response = requests.get('http://127.0.0.1:5000/users/1')

# response = requests.patch('http://127.0.0.1:5000/users/1',
#                          json={'password': '1234'})

# response = requests.delete('http://127.0.0.1:5000/users/3')
#
response = requests.post('http://127.0.0.1:5000/announcment',
                         json={
                             'title': 'Второй заголовок',
                             'description': 'Какое-то описание',
                             'owner': 1,
                             'password': '1234'
                         })

# response = requests.get('http://127.0.0.1:5000/announcment/2')

# response = requests.patch('http://127.0.0.1:5000/announcment/1',
#                          json={
#                              'title': 'Новый заголовок',
#                              'description': 'Какое-то описание',
#                              'password': '1234'
#                          })
# response = requests.delete('http://127.0.0.1:5000/announcment/2',
#                          json={
#                              'owner': 1,
#                              'password': '1234'
#                          })

print(response.status_code)
print(response.json())