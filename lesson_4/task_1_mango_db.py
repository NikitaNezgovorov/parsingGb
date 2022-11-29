"""
Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет добавлять
только новые вакансии/продукты в вашу базу.

* Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
(необходимо анализировать оба поля зарплаты).

* Любая аналитика. Например matching ваканский с разных площадок
"""
from pprint import pprint

import pandas as pd
from pymongo import MongoClient

URL = 'https://hh.ru/search/vacancy'
AREA = 1844
text = 'python'
items_on_page = 20

params = {
    'area': AREA,
    'text': text,
    'items_on_page': items_on_page,
    'page': 0,
}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 "
                  "Safari/537.36 "
}

client = MongoClient('mongodb://127.0.0.1:27017/')
print(client.list_database_names())
db = client.parse_hh_db
db_vacancies = db.vacancies


# hh_parse_list_vacancies = hh_bs_parse(url=URL, params=params, headers=headers)


def add_vacancy(vacancies, vacancies_db):
    new_vacancy_count = 0
    for vacancy in vacancies:
        if vacancies_db.count_documents({'vacancy_link': vacancy['vacancy_link']}, limit=1) == 0:
            vacancies_db.insert_one(vacancy)
            print(f'Новая вакансия "{vacancy["vacancy_name"]}" добавлена')
            new_vacancy_count += 1
        else:
            print(f'Вакансия "{vacancy["vacancy_name"]}" уже добавлена')
    vacancies_in_db = vacancies_db.find()
    pprint(f'Добавлено {new_vacancy_count} записей. Количество вакансий {len(list(vacancies_in_db))}')


def search_vacancy_by_salary(vacancies_db):

    while True:
        try:
            salary_needed = int(input('input needed salary - '))
            break
        except ValueError:
            print('Wrong input, value must be integer')
    searched_vacancies = vacancies_db.find(
        {'$or': [{'min_salary': {'$gte': salary_needed}}, {'max_salary': {'$gte': salary_needed}}]})

    return searched_vacancies


if __name__ == "__main__":
    # add_vacancy(vacancies=hh_bs_parse(url=URL, params=params, headers=headers), vacancies_db=db_vacancies)
    ds = (search_vacancy_by_salary(db_vacancies))
    df = pd.DataFrame(list(ds))
    df.to_excel('search.xlsx')
