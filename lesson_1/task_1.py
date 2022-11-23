"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
 сохранить JSON-вывод в файле *.json.
"""
import requests
import json
from pprint import pprint


user = 'NikitaNezgovorov'
url = f'https://api.github.com/users/{user}/repos'
response = requests.get(f'{url}')
pprint(response.status_code)
repos = response.json()
pprint(repos)

with open('repos.json', 'w', encoding='UTF-8') as f:
    for repo in repos:
        pprint(repo['name'])
        json.dump(repo['name'], f)

