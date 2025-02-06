import requests
from bs4 import BeautifulSoup

from logger import Logger


class Scrapper:
    @staticmethod
    def scrape_affiliation(url):
        Logger.log(f'Scrapping affiliation {url}')
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        return {
            'name': url.split('/')[-1],
            'users': Scrapper.parse_users(soup),
        }

    @staticmethod
    def parse_users(soup):
        users = []
        rows = soup.find('tbody').find_all('tr')
        Logger.log(f'Found {len(rows)} users')

        for row in rows:
            tds = row.find_all('td')
            if len(tds) == 5:
                users.append({
                    'rank': int(tds[0].text),
                    'user': tds[1].find('a').text,
                    'country': None if tds[2].find('a') is None else tds[2].find('a')['title'],
                    'subdivision': None if tds[3].find('a') is None else tds[3].find('a')['title'],
                    'score':  float(tds[4].text),
                    'nickname': tds[1].find('a')['href'].split('/')[-1],
                })
            Logger.log(f'Processed {users[-1]["nickname"]}')

        return users
