# Написать приложение, которое собирает основные новости с сайта yandex.ru.
# Новости экономики

from lxml import html
import requests
from pprint import pprint
import pandas as pd
from datetime import date

url = 'https://yandex.ru/news/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

news = []
current_date = str(date.today())

items = dom.xpath('//div[contains(@class, "mg-grid__col")]/article')

for item in items:
    one_news = {}

    link = item.xpath('.//div[@class="mg-card__text"]/a/@href')
    name_ = str(item.xpath('.//h2[@class="mg-card__title"]/text()'))
    name = name_.replace(u'\\xa0', u' ')
    time = item.xpath('.//span[@class="mg-card-source__time"]/text()')

    one_news['name'] = name
    one_news['link'] = link
    one_news['day'] = current_date
    one_news['time'] = time
    one_news['url'] = url

    news.append(one_news)

pprint(news)

df = pd.DataFrame(columns=('name', 'link', 'day', 'time', 'url'))

for row in news:
    df.loc[len(df)] = row

df.to_csv('yandex_news', encoding='utf-8', index=False)
