"""
2. Работа будет состоять с недокументированным API. Нужно ввести релевантный запрос на сайте https://www.delivery-club.ru/search
(а) из предложенных точек с помощью API найти долю (в %) с бесплатной и платной доставкой. Для каждой категории рассчитать среднюю минимальную стоимость заказа.
(б) для каждой из категорий из пункта (а) рассчитать долю (в %) магазинов и ресторанов
"""

from collections import defaultdict
from pprint import pprint

import requests

params = {
    'latitude': '55.7577374',
    'longitude': '37.6164793',
    'query': 'манты'
}

url = 'https://api.delivery-club.ru/api1.2/vendors/search'

response = requests.get(url, params=params)
vendor_list = response.json()['vendors']

print(response.url)
pprint(response.status_code)


# pprint(vendor_list)


def category_find(vendors):
    category_list = []
    for vendor in vendors:
        category_list.append(vendor['categoryId'])
    return set(category_list)


def category_share(vendors_categories, categories_dict):
    for key in dict(vendors_categories):
        categories_dict[key] = (len(vendors_categories[key]))
    sum_of_categories = sum(categories_dict.values())
    for key in categories_dict:
        print(f'Доля категории {key} - {categories_dict[key] / sum_of_categories * 100}%')


print(category_find(vendor_list))


def free_delivery_percent(vendors):
    free_delivery_count = 0
    min_price_count_free_delivery = 0
    min_price_count_paid_delivery = 0
    free_delivery_vendors_categories = defaultdict(list)
    free_delivery_categories_dict = {}
    paid_delivery_vendors_categories = defaultdict(list)
    paid_delivery_categories_dict = {}
    for vendor in vendors:
        if vendor['delivery']['price']['value'] == 0:
            free_delivery_count += 1
            min_price_count_free_delivery += vendor['delivery']['minOrderPrice']['value']
            free_delivery_vendors_categories[vendor['categoryId']].append(vendor['name'])
        else:
            min_price_count_paid_delivery += vendor['delivery']['minOrderPrice']['value']
            paid_delivery_vendors_categories[vendor['categoryId']].append(vendor['name'])

    free_delivery_share = round((free_delivery_count / len(vendors) * 100), 2)
    free_delivery_min_price = round((min_price_count_free_delivery / free_delivery_count), 2)
    paid_delivery_share = round((100 - free_delivery_share), 2)
    paid_delivery_min_price = round((min_price_count_paid_delivery / (len(vendors) - free_delivery_count)), 2)
    print('Бесплатная доставка')
    category_share(free_delivery_vendors_categories, free_delivery_categories_dict)
    print('Платная доставка')
    category_share(paid_delivery_vendors_categories, paid_delivery_categories_dict)

    return print(
        f'Доля заведений с бесплатной доставкой {free_delivery_share}% Средняя цена минимального заказа {free_delivery_min_price} \nДоля заведений с платной доставкой {paid_delivery_share}% Cредняя цена минимального заказа {paid_delivery_min_price}')


free_delivery_percent(vendor_list)
