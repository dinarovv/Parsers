import csv
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS

import requests
import lxml

class Parser:

    def __init__(self):

        self.url = 'https://hidexn.name/proxy-list/?start='
        self.user_agent = UserAgent()
        self.proxy_list = []
        self.page_count = 0


    def get_page_count(self): # получение количества страниц

        headers = {'user-agent': self.user_agent.random}
        response = requests.get(url=self.url, headers=headers)
        self.page_count = int([item.text for item in BS(response.text, 'lxml') \
                              .find('div', class_='pagination').find_all('a')][-2])

    def parse(self): # парсинг

        self.get_page_count()

        print('Начинаю парсинг сайта...')

        for index in range(0, self.page_count):

            print(f'Анализирую {index + 1} страницу...')

            headers = {'user-agent': self.user_agent.random}
            url = f'{self.url}{index * 64}#list'
            response = requests.get(url=url, headers=headers)
            soup = BS(response.text, 'lxml').find('table').find_all('td')

            counter, proxy = 0, []

            for item in soup[7:]:

                counter += 1
                proxy.append(item.text)

                if counter == 7:

                    self.proxy_list.append(proxy)
                    counter = 0
                    proxy = []

        print('Парсинг данных завершён.')


    def create_csv(self): # создание + заполнение *.csv

        with open('proxies.csv', 'w', encoding='utf-8-sig', newline='') as file:

            writer = csv.writer(file, delimiter=';')
            writer.writerow(['IP адрес', 'Порт', 'Страна, Город', 'Скорость', 'Тип',
                             'Анонимность', 'Последнее обновление'])

        with open('proxies.csv', 'a', encoding='utf-8-sig', newline='') as file:

            writer = csv.writer(file, delimiter=';')

            for proxy in self.proxy_list:
                writer.writerow(proxy)

        print('Данные переданы в csv таблицу.')
        file.close()


    def create_txt(self): # создание + заполнение *.txt

        with open("proxies.txt", "w", encoding="utf-8") as file:

            for proxy in self.proxy_list:
                short_proxy = f'{proxy[0]}:{proxy[1]}'
                file.write(f'{short_proxy}\n')

        print('Данные переданы в текстовый файл.')
        file.close()


    def parse_csv(self):

        self.parse()
        self.create_csv()


    def parse_txt(self):

        self.parse()
        self.create_txt()


    def parse_txt_csv(self):

        self.parse()
        self.create_txt()
        self.create_csv()
        

if __name__ == '__main__':
    
    parser = Parser()
    parser.parse_txt_csv() # - для всего
    #parser.parse_txt() # - для *.txt
    #parser.parse_csv() # - для *.csv
