# Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
from pprint import pprint
import json

num_name = int(input('Введите 0, если хотите список для организаций; введите 1, если хотите список для человека: '))
username = input('Введите имя пользователя: ')

if num_name == 1:
    url = 'https://api.github.com/users/'+username+'/repos'
else:
    url = 'https://api.github.com/orgs/'+username+'/repos'

response = requests.get(url)
j_data = response.json()
pprint(j_data)
repos = []
for i in j_data:
    repos.append(i['name'])

pprint(f'Список репозиториев для {username}: {repos}')

with open('data.json', 'w') as f:
    json.dump(j_data, f)

