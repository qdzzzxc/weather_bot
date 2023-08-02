from selenium import webdriver
from selenium.common import TimeoutException
from lxml import html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import json
from datetime import datetime


with open('memo_cords_file.json') as json_file:
    memo_info = json.load(json_file)


def save_json():
    with open('memo_cords_file.json', 'w') as outfile:
        json.dump(memo_info, outfile)


def get_cords(name):
    name = name.lower()
    if name in memo_info:
        return memo_info[name]['cords'][0], memo_info[name]['cords'][1]
    driver = webdriver.Firefox()
    driver.get("https://yandex.ru/maps")
    elem = driver.find_element(By.CSS_SELECTOR,'input.input__control._bold')
    elem.send_keys(name)
    time.sleep(2)
    elem = driver.find_element(By.XPATH, '//span[@class = "input__context"]/input')
    elem.send_keys(Keys.ENTER)
    try:
        elem = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH,'//div[@class = "toponym-card-title-view__coords-badge"]')))
    except TimeoutException:
        driver.find_element(By.XPATH,'//*[@class="business-contacts-view__address-link"]').click()
        elem = driver.find_element(By.XPATH, '//div[@class = "toponym-card-title-view__coords-badge"]')
    result = elem.text.split()
    driver.quit()
    memo_info[name] = {'cords': (result[0][:-2], result[1])}
    return result[0][:-2], result[1]


def get_weather_yandex_now(name,lat,lon):
    url = 'https://yandex.ru/pogoda/'
    resp = requests.get(url, params={'lat':lat,'lon':lon})
    tree_for_temp = html.fromstring(resp.content)
    temp = tree_for_temp.xpath(f'//*[@class ="temp__value temp__value_with-unit"]/text()')
    #if temp: темп пустой если капча не пройдена
    memo_info[name]['temp_now'] = temp[1:3]
    memo_info[name]['temp_for_10_days'] = temp[5:25:2]
    memo_info[name]['last_time_upd'] = str(datetime.now()).split()[1].split(':')[:2]


def get_stat(name):
    if name in memo_info:
        h_now, min_now = str(datetime.now()).split()[1].split(':')[:2]
        h_upd, min_upd = memo_info[name]['last_time_upd']
        if abs(int(h_now) - int(h_upd)) <= 2 and memo_info[name]['temp_now']:
            return memo_info[name]
    lat, lon = get_cords(name)
    get_weather_yandex_now(name, lat, lon)
    save_json()
    return memo_info[name]


#print(get_stat('сушкинская'))