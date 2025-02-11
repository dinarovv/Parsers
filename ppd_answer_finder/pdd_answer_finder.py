from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS
import requests
import lxml


class Parser:

    def __init__(self, questions):
        self.questions = questions
        self.questions_list = []
        self.url = 'https://biletpdd.ru/bilety/ab/'
        self.user_agent = UserAgent()
        self.answers = []


    def parse(self):

        for index in range(1,29):

            print(f'Поиск по теме {index}...')
            theme_url = f'{self.url}tema{index}.htm'
            headers = {
                'user-agent': self.user_agent.random,
            }
            response = requests.get(url = theme_url, headers = headers)
            soup = BS(response.text, 'lxml')
            card = soup.find_all('div', class_='question')

            for item in card:

                #question_url = f'https://biletpdd.ru{item.find('a').get('href')}' - получение ссылки на вопрос
                question = ' '.join(item.text.strip().split('\n')[2].split())
                answer = item.find('li', class_ = 'right').text
                self.answers.append({question : answer})

        print('Парсинг данных завершен.')


    def write_txt_report(self):

        with open("answers.txt", "w", encoding = "utf-8") as txt:
            for my_question in self.questions_list:
                counter = 0
                for dictionary in self.answers:
                    if list(dictionary.keys())[0] == my_question:
                        counter += 1
                        if counter > 1:
                            txt.write(f'    Найден еще один ответ: {list(dictionary.values())[0]}\n')
                        else:
                            txt.write(f'{list(dictionary.values())[0]}\n')

                if counter == 0:
                    txt.write('Нету ответов на данный вопрос.\n')
        print('Ответы были переданы в "answers.txt"')


    def get_txt_questions(self):
        with open(self.questions, 'r', encoding = 'utf-8') as file:
            self.questions_list = [line.strip() for line in file]
            print('Файл с вопросами получен.')


    def start(self):
        self.get_txt_questions()
        self.parse()
        self.write_txt_report()

if __name__ == '__main__':
    parser = Parser('questions.txt')
    parser.start()
