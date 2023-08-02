from lxml import html
import requests
from transliterate import translit
import mechanicalsoup

def get_city_name(name):
    return translit(name, language_code='ru', reversed=True).lower()

def get_city_cords_2(name):
    cords_url = 'https://time-in.ru/coordinates/'
    resp = requests.get(cords_url, headers = {'search':name})
    print(resp.url)
    tree_for_cords = html.fromstring(resp.content)
    cords = tree_for_cords.xpath(f'//div[@class="coordinates-city-info"]/div/text()')[0].split()
    lat = cords[2][:-2]
    lon = cords[3]
    return lat, lon

city_cords_memo = {}
def get_city_cords(name):
    if name in city_cords_memo:
        return city_cords_memo[name]
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("https://yandex.ru/maps")
    print(browser.url)
    browser.select_form('form.search-form-view')
    print(browser.form.print_summary())
    browser["value"] = name
    browser.submit_selected()

    print(browser.get_current_page())


get_city_cords('Одинцово')