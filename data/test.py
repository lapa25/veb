from requests import get, post, delete

print(get('http://localhost:5000/api/v2/users').json())  # коректный запрос на получение всех пользователей
print(get('http://localhost:5000/api/v2/users/1').json())  # коректный запрос на получение пользователя по id
print(get('http://localhost:5000/api/v2/users/555').json())  # несуществующий id при получении пользователя
print(delete('http://localhost:5000/api/v2/users/4').json())  # коректный запрос на удаление пользователя по id
print(delete('http://localhost:5000/api/v2/users/55').json())  # несуществующий id при удалении
print(delete('http://localhost:5000/api/v2/users').json())  # нет id при удалении
print(post('http://localhost:5000/api/v2/users',  # коректный запрос на добавление пользователя
           json={'name': 'Antonina',
                 'surname': 'Lapa',
                 'age': 15,
                 'position': 'programmer',
                 'speciality': 'programmer',
                 'address': 'module_1',
                 'email': 'alapa@mars.org'}
           ).json())
print(post('http://localhost:5000/api/v2/users',  # отсутвие аргументов при добавлении
           ).json())
print(post('http://localhost:5000/api/v2/users',  # не все аргументы переданы при добавлении
           json={'name': 'Antonina',
                 'surname': 'Lapa',
                 'age': 15,
                 'position': 'programmer',
                 'speciality': 'programmer'}
           ).json())
