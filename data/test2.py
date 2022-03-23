from requests import get, post, delete

print(get('http://localhost:5000/api/v2/jobs').json())  # коректный запрос на получение всех работ
print(get('http://localhost:5000/api/v2/jobs/1').json())  # коректный запрос на получение работы по id
print(get('http://localhost:5000/api/v2/jobs/555').json())  # несуществующий id при получении работы
print(delete('http://localhost:5000/api/v2/jobs/3').json())  # коректный запрос на удаление работы по id
print(delete('http://localhost:5000/api/v2/jobs/55').json())  # несуществующий id при удалении работы
print(delete('http://localhost:5000/api/v2/jobs').json())  # нет id при удалении
print(post('http://localhost:5000/api/v2/jobs',  # коректный запрос на добавление работы
           json={'job': 'testing',
                 'team_leader': 2,
                 'collaborators': '3,4',
                 'work_size': 10,
                 'is_finished': False}
           ).json())
print(post('http://localhost:5000/api/v2/jobs',  # отсутвие аргументов при добавлении
           ).json())
print(post('http://localhost:5000/api/v2/jobs',  # не все аргументы переданы при добавлении
           json={'job': 'testing',
                 'collaborators': '3,4',
                 'work_size': 10,
                 'is_finished': False}
           ).json())
