"""
2. Работа будет состоять с недокументированным API. Нужно ввести релевантный запрос на сайте https://www.delivery-club.ru/search
(а) из предложенных точек с помощью API найти долю (в %) с бесплатной и платной доставкой. Для каждой категории рассчитать среднюю минимальную стоимость заказа.
(б) для каждой из категорий из пункта (а) рассчитать долю (в %) магазинов и ресторанов
"""
from pprint import pprint

import requests

params = {
    'latitude': '55.7577374',
    'longitude': '37.6164793',
    'query': 'манты'
}

url = 'https://api.delivery-club.ru/api1.2/vendors/search'

response = requests.get(url, params=params)
vendors = response.json()['vendors']

# pprint(response.json()['vendors'])

free_delivery_count = 0
for vendor in vendors:
    if vendor['delivery']['price']['value'] == 0:
        free_delivery_count += 1
free_delivery_share = free_delivery_count/len(vendors) * 100
paid_delivery_share = 100 - free_delivery_share

print(f'Доля заведений с бесплатной доставкой {free_delivery_share}% \nДоля заведений с платной доставкой {paid_delivery_share}%')
