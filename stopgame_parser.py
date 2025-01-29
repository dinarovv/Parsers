import requests
import json
import lxml

from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

class Parser:

    def __init__(self):
        
        self.url = 'https://stopgame.ru/'
        self.comments = dict()

    def parse(self):

        user_agent = UserAgent()

        url = f'{self.url}/news'
        headers = {'User-Agent': user_agent.random}

        response = requests.get(url = url, headers = headers)
        last_page = int([item.text for item in BS(response.text, 'lxml').find_all('a', class_ = 'item')][-1])

        input_value = int(input(f'''\
Введите:
- Любое количество страниц (0 < x <= {last_page})
- 0, чтобы пропарсить все {last_page} страницы (это очень долго, поверьте)
Ввод: \
'''))
        last_page = input_value if input_value != 0 else last_page

        for page in range(1, last_page + 1):

            print(f'Парсинг страницы {page}...')

            page_url = f'{self.url}/news/all/p{page}/'
            headers = {'User-Agent': user_agent.random}

            response = requests.get(url = page_url, headers = headers)
            items = [item.get('data-key') for item in BS(response.text, 'lxml').find_all('div') if item.get('data-key') is not None]

            for item in items:

                news_url = f'{self.url}newsdata/{item}/'

                response = requests.get(url = news_url, headers = headers)

                news_name = BS(response.text, 'lxml').find('h1').text
                soup = BS(response.text, 'lxml')

                authors = [(str(i).split('<')[-2]).split('>')[-1] \
                           for i in soup.find('section', \
                                class_ = '_page-section_dhept_478 _section_5hrm4_6 _comments-container_5hrm4_1695')\
                               .find_all('span', class_ = '_user-info__name_dhept_1165')]
                comments = [i.text.strip() for i in soup.find_all('div', class_ = '_comment__body_1n88f_1')]

                for a, c in zip(authors, comments):

                    if news_name in self.comments:

                        self.comments[news_name][a] = c.replace('\r','')

                    else:

                        self.comments[news_name] = {a: c.replace('\r','')}


    def write_json(self):

        with open('comments.json', 'w', encoding = 'utf-8') as file:

            json.dump(self.comments, file, indent = 4, ensure_ascii = False)

            print(f'Ваш "*.json" готов к использованию!')


    def parse_json(self):

        self.parse()
        self.write_json()


if __name__ == '__main__':
    
    parser = Parser()
    parser.parse_json()
