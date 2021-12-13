# Написать программу, которая собирает товары "В тренде"
# с сайта техники mvideo и складывает данные в БД.

from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from pymongo import MongoClient
from pymongo.errors import *

url = 'https://www.mvideo.ru'
chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome("./chromedriver.exe", options=chrome_options)
driver.implicitly_wait(10)

driver.get(url)

driver.execute_script("scroll(0, 1600)")
time.sleep(5)
button = driver.find_element(By.XPATH, "//span[@class='title'][text()=' В тренде ']").click()

name_list = driver.find_elements(By.XPATH,
                                "//mvid-shelf-group//div[@class='product-mini-card__name ng-star-inserted']")
price_list = driver.find_elements(By.XPATH,
                                 "//mvid-shelf-group//div[@class='product-mini-card__price ng-star-inserted']")

items = []
goods = list(zip(name_list, price_list))
for good in goods:
    item = {}
    name = good[0].text
    price = good[1].find_element(By.CLASS_NAME, 'price__main-value').text
    link = good[0].find_element(By.XPATH, ".//a").get_attribute('href')

    item['name'] = name
    item['price'] = price
    item['link'] = link

    items.append(item)

pprint(items)

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
trend_goods = db.trend_goods

db.vacancy_hh.create_index([('name', 1), ('link', 1)], unique=True)   # уникальный id по name и link

for i in items:
    try:
        trend_goods.insert_one(i)
    except DuplicateKeyError:
        break



