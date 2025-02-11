import time
import json
import emoji

from selenium import webdriver
from selenium.webdriver.common.by import By

class Parser:

    def __init__(self):

        self.url: str = 'https://www.youtube.com/'
        self.keyword: str = ''
        self.count: int = 0
        self.titles: list[str] = []
        self.urls: list[str] = []
        self.authors: list[str] = []
        self.info: list[str] = []
        self.tags: list[list[str]] = []


    def set_keyword(self):

        self.keyword = input('Введите любую тему видео: ')


    def set_count(self):

        self.count = int(input('Введите количество видео: '))


    def parse(self):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-gpu")


        with webdriver.Chrome(options = chrome_options) as browser:

            browser.get(self.url)

            try:
                # принятие куки
                browser.find_element(By.XPATH,
                '/html/body/ytd-app/ytd-consent-bump-v2-lightbox/' +\
                'tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape').click()
                time.sleep(1)

            except Exception as _ex:

                pass

            xpath = [
    '/html/body/ytd-app/div[1]/div[2]/ytd-masthead/div[4]/div[2]/yt-searchbox/button',
    '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div' + \
    '/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div/div/ytd-toggle-button-renderer/' + \
    'yt-button-shape/button/yt-touch-feedback-shape/div/div[2]',
    '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/' + \
    'ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div/tp-yt-iron-collapse/div/' + \
    'ytd-search-filter-group-renderer[2]/ytd-search-filter-renderer[1]/a',
    '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/' + \
    'div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div/tp-yt-iron-collapse/div/' + \
    'ytd-search-filter-group-renderer[5]/ytd-search-filter-renderer[3]/a/div/yt-formatted-string',
    '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/' + \
    'div/div[4]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[1]',
    '//*[@id="description-inner"]',
    '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/div/ytd-search-header-renderer/div[3]',
    '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-search-filter-options-dialog-renderer/div[2]/' +\
    'ytd-search-filter-group-renderer[2]/ytd-search-filter-renderer[1]/a',
    '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-search-filter-options-dialog-renderer/div[2]/' +\
    'ytd-search-filter-group-renderer[5]/ytd-search-filter-renderer[3]/a',
            ]

            browser.find_element(By.TAG_NAME, 'input').click()
            time.sleep(1)
            browser.find_element(By.TAG_NAME, 'input').send_keys(self.keyword)
            time.sleep(1)
            browser.find_element(By.XPATH, xpath[0]).click()
            time.sleep(1)

            try:
                # для русского интерфейса
                browser.find_element(By.XPATH, xpath[1]).click()
                time.sleep(1)
                browser.find_element(By.XPATH, xpath[2]).click()
                time.sleep(1)
                browser.find_element(By.XPATH, xpath[1]).click()
                time.sleep(1)
                browser.find_element(By.XPATH, xpath[3]).click()
                time.sleep(1)

            except Exception as _ex:
                # в остальных случаях
                browser.find_element(By.XPATH, xpath[6]).click()
                time.sleep(1)
                browser.find_element(By.XPATH, xpath[7]).click()
                time.sleep(1)
                browser.find_element(By.XPATH, xpath[6]).click()
                time.sleep(1)
                browser.find_element(By.XPATH, xpath[8]).click()
                time.sleep(1)

            browser.execute_script(f"window.scrollBy(0,{275})")

            if round(self.count / 19) != 0:

                for _ in range (round(self.count / 19 * 2)):

                    browser.execute_script(f"window.scrollBy(0,{250 * 25})")
                    time.sleep(1)

            count = 0

            for video in browser.find_elements(By.XPATH, '//*[@id="thumbnail"]/yt-image/img'):

                flag = True
                while flag:

                    try:
                        video.click()
                        time.sleep(1)
                        flag = False

                    except Exception as _ex:

                        browser.execute_script(f"window.scrollBy(0,250)")

                video_url = browser.current_url
                self.urls.append(video_url)
                self.titles.append(browser.find_element(By.CSS_SELECTOR, "h1.style-scope.ytd-watch-metadata").text)
                self.authors.append(browser.find_element(By.CSS_SELECTOR, "yt-formatted-string.ytd-channel-name a").text)

                try:

                    if count < self.count:

                        video.find_element(By.XPATH, xpath[4]).click()
                        time.sleep(1)
                        count += 1

                        for items in browser.find_elements(By.XPATH, xpath[5]):

                            print(f'Собираем информацию о {video_url}... ({int(count/self.count * 100)}%)')

                            tags = items.text.split()
                            video_info = items.text.split('г.')

                            if 'авг.' not in items.text:

                                self.info.append(f'{video_info[0].strip()}г.')

                            else:

                                self.info.append(f'{video_info[0].strip()}г.{video_info[1].strip()}г.')

                            video_tags = [emoji.replace_emoji(tag, replace="") for tag in tags if '#' in tag]
                            # удаление эмодзи методом библиотеки emoji, во избежании таких тегов: "🥶🥶#subscribe"
                            self.tags.append(list(set(video_tags)))

                            browser.back()
                            browser.execute_script(f"window.scrollBy(0,250)")

                    else:

                        print(f'Была собрана информация о {len(self.info)} видео.')
                        return 0

                except Exception as _ex:

                    browser.back()
                    browser.execute_script("window.scrollBy(0,250)")
                    time.sleep(1)
                    continue

            print(f'Была собрана информация о {len(self.info)} видео.')


    def make_json(self):

        with open('youtube_tag_analyzer.json', 'w', encoding='utf-8') as file:

            tagz = dict()

            for author, title, url, info, tags in zip(self.authors, self.titles, self.urls, self.info, self.tags):

                if (author != '' or author != ' ') and (title != '' or title != ' '):
                    tagz[f'{author} - {title} ({url})'] = {info : tags}

                else:
                    tagz[f'|shorts_video| ({url})'] = {info: tags}

            json.dump(tagz, file, indent=4, ensure_ascii=False)
            print('Создан *.json отчет.')


    def make_txt(self):

        tags = []

        for items in self.tags:

            for item in items:

                tags.append(item)

        tags = set(tags)

        with open('youtube_tag_analyzer.txt', 'w', encoding='utf-8') as file:

            file.write('')

        with open('youtube_tag_analyzer.txt', 'a', encoding='utf-8') as file:

            for tag in tags:

                file.write(f'{tag} ')

        print('Создан *.txt отчет.')



    def parse_all(self):

        self.set_keyword()
        self.set_count()
        self.parse()
        self.make_json()
        self.make_txt()


if __name__ == '__main__':

    parser = Parser()
    parser.parse_all()
