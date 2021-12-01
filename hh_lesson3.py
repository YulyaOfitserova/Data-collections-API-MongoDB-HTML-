#Необходимо собрать информацию о вакансиях на вводимую должность
#(используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
#Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
#Получившийся список должен содержать в себе минимум:
#Наименование вакансии.
#Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
#Ссылку на саму вакансию.
#Сайт, откуда собрана вакансия.
#По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
#Структура должна быть одинаковая для вакансий с обоих сайтов.
#Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.

import requests
from pprint import pprint
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
from enum import unique
from pymongo import MongoClient
from pymongo.errors import *

url = 'https://hh.ru'

params = {'area': '113', 'clusters': 'true',
          'enable_snippets': 'true', 'experience': 'noExperience',
          'ored_clusters': 'true', 'schedule': 'remote',
          'text': 'Analytics', 'from': 'suggest_post', 'page': ''}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
response = requests.get(url + '/search/vacancy', params=params, headers=headers)

dom = BeautifulSoup(response.text, 'html.parser')

pages = dom.find_all('a', {'class': 'bloko-button'})[-2]
num_page = int(pages.text)

vacancy = dom.find_all('div', {'class', 'vacancy-serp-item'})

vacancy_list = []
for p in range(num_page):
    params['page'] = p
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancy = dom.find_all('div', {'class', 'vacancy-serp-item'})
    for vac in vacancy:
        vacancy_data = {}
        name = vac.find('a')
        link = name.get('href')
        name = name.text
        salary = vac.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary:
            salary_min = None
            salary_max = None
            currency = None
        else:
            salary = salary.getText().replace(u'\u202f', u'')
            salary_list = salary.split(' ')

            if salary_list[0] == 'от':
                salary_min = int(salary_list[1])
                salary_max = None
                currency = salary_list[2]
            elif salary_list[0] == 'до':
                salary_max = int(salary_list[1])
                salary_min = None
                currency = salary_list[2]
            else:
                salary_min = int(salary_list[0])
                salary_max = int(salary_list[2])
                currency = salary_list[3]

        vacancy_data['name'] = name
        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['link'] = link
        vacancy_data['currency'] = currency
        vacancy_data['url'] = url

        vacancy_list.append(vacancy_data)
        p += 1


df = pd.DataFrame(columns=('name', 'link', 'salary_min', 'salary_max', 'currency', 'url'))

for row in vacancy_list:
    df.loc[len(df)] = row

print(df)

df.to_csv('hh', encoding='utf-8', index=False)

# дз к третьему уроку

client = MongoClient('127.0.0.1', 27017)
db = client['hh']
vacancy_hh = db.vacancy_hh
db.vacancy_hh.create_index([('name', 1), ('link', 1)], unique=True)   # уникальный id по name и link
# vacancy_hh.insert_many(vacancy_list)

for doc in vacancy_hh.find({'$or': [{'salary_min': {'$gte': 50000}}, {'salary_max': {'$gt': 50000}}]}):
    pprint(doc)

new_data = {'name': "Investigation Analyst",
            'salary_min': 1000,
            'salary_max': 2000,
            'link':"https://odintsovo.hh.ru/vacancy/49798188?from=vacancy_search_list&quer...",
            'currency': "USD",
            'url': "https://hh.ru"}
try:
    vacancy_hh.insert_one(new_data)
except DuplicateKeyError as e:
    print(e)

