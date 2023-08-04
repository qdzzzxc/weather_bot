import asyncio
import time
from aiohttp import ClientSession
from lxml import html
from bs4 import BeautifulSoup as bs


async def get_open_weather(city):
    async with ClientSession() as session:
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56', 'units':'metric'}

        async with session.get(url=url, params=params) as response:
            weather = await response.json()
            if weather.get('message'):
                return
            return weather['name'], weather['coord']['lat'], weather['coord']['lon'], weather['weather'][0]['main'], \
                weather['main']['temp'], weather['main']['feels_like']


async def get_yandex_weather(lat,lon):
    async with ClientSession() as session:
        url = 'https://yandex.ru/pogoda/'
        params = {'lat':lat,'lon':lon}

        async with session.get(url=url, params=params) as response:
            tree_for_temp = html.fromstring(await response.text())
            temp = tree_for_temp.xpath(f'//*[@class ="temp__value temp__value_with-unit"]/text()')
            return temp[1], temp[2], temp[5:25:2]

async def get_mail_weather(name):
    async with ClientSession() as session:
        url = 'https://pogoda.mail.ru/prognoz/' + f'{name}/'
        async with session.get(url=url) as response:
            soup = bs(await response.text(), 'html.parser')
            for_10_days = soup.findAll('div', class_="day__temperature")
            for_10_days = [x.get_text()[1:3] for x in for_10_days]
            print(for_10_days)



async def get_stat(city):
    open_weather = await asyncio.create_task(get_open_weather(city))
    if not open_weather:
        return
    name, lat, lon = open_weather[0], open_weather[1], open_weather[2]
    #print(await asyncio.create_task(get_yandex_weather(lat,lon)))
    #print(await asyncio.create_task(get_mail_weather(name)))
    return open_weather

#asyncio.run(get_stat('голицыно'))
