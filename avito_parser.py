import requests
from bs4 import BeautifulSoup as BS

def parse(my_region: str, favorite_section: str):
    '''
    Простой парсер разделов сайта Авито
    ---Как пользоваться---
    вызываем функцию parse() от:
    1) СВОЕГО города английским транслитом. (Пример: 'moscva', 'chelyabinsk', ...) (P.S. От чужого города не работает!!!)
    2) Названия одного из разделов Авито. (Пример: 'tovary_dlya_kompyutera', 'bytovaya_elektronika', ...)
    ----------------------
    Используется юзер агент (без него все тоже может рабоать). Он нужен для свободного посещения сайта в статусе юзера, а не бота.
    Парсер преобразует содержимое страницы в объект (soup), который можно использовать для поиска HTML-элементов.
    HTML - классы переданы в код путём анализа кода элемента страницы (f12).
    Каждое объявление помещается в список товаров словарём вида: {ключ - название предмета/услуги: предмет - цена}.
    '''
    url = f'https://www.avito.ru/{my_region}/{favorite_section}'
    headers = {
        'User-Agent' : ''
    }
    response = requests.get(url, headers = headers)
    soup = BS(response.content, 'html.parser')
    items = soup.findAll('div', class_  = 'iva-item-content-OWwoq')
    comps = []

    for item in items:
        key = item.find('a', class_ = "styles-module-root-m3BML styles-module-root_noVisited-HHF0s").get_text(strip = True)
        item = item.find('p', class_ = 'styles-module-root-s4tZ2 styles-module-size_l-j3Csw styles-module-size_l_dense-JjSpL styles-module-size_l-ai2ZG styles-module-size_dense-uclxr stylesMarningNormal-module-root-_xKyG stylesMarningNormal-module-paragraph-l-dense-v8hof').get_text(strip = True).replace('\xa0', '')
        comps.append({
             key : item
        })

    for comp in comps:
        for item, price in comp.items():
            print(f'{item}: {price}')

if __name__ == '__main__':
    region: str = 'chelyabinsk'
    section: str = 'tovary_dlya_kompyutera'
    parse(my_region= region, favorite_section= section)