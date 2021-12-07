# Написать приложение, которое собирает основные новости с сайта news.mail.ru.
# Новости экономики

from lxml import html
import requests
from pprint import pprint
import pandas as pd

url = 'https://news.mail.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

response = requests.get('https://news.mail.ru/economics/', headers=headers)

dom = html.fromstring(response.text)

news = []
items = dom.xpath("//a[contains(@class, 'newsitem') and not(contains(@name, 'n'))]")  # исключаем динамическую новость, которая не относится к экономике

i = 0
for item in items:
    one_news = {}

    link = dom.xpath(".//a[contains(@class, 'newsitem') and not(contains(@name, 'n'))]/@href")[i]
    name = dom.xpath(".//a[contains(@class, 'newsitem') and not(contains(@name, 'n'))]/span/text()")[i]
    datetime = dom.xpath(".//span[@class='newsitem__param js-ago']/@datetime")[i]

    one_news['name'] = name
    one_news['link'] = link
    one_news['datetime'] = datetime
    one_news['url'] = url

    news.append(one_news)
    i += 1

pprint(news)

df = pd.DataFrame(columns=('name', 'link', 'datetime', 'url'))

for row in news:
    df.loc[len(df)] = row

df.to_csv('news_mail', encoding='utf-8', index=False)
