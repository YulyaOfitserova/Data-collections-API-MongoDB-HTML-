from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome("./chromedriver.exe")

driver.get("https://account.mail.ru/login/")


print()
