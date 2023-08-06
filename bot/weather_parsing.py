import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs


async def get_open_weather(city):
    async with ClientSession() as session:
        url = f'http://api.openweathermap.org/data/2.5/weather'
        APIkey = '2a4ff86f9aaa70041ec8e82db64abf56'
        params = {'q': city, 'APPID': APIkey, 'units':'metric'}

        async with session.get(url=url, params=params) as response:
            weather = await response.json()
            if weather.get('message'):
                return
            name = weather['name']
            lat = weather['coord']['lat']
            lon = weather['coord']['lon']
            type_ = weather['weather'][0]['main']
            temp_now = weather['main']['temp']
            feels_like = weather['main']['feels_like']

            return name, lat, lon, type_, temp_now, feels_like


async def get_yandex_weather(lat,lon):
    async with ClientSession() as session:
        url = 'https://yandex.ru/pogoda/'
        params = {'lat':lat,'lon':lon}

        async with session.get(url=url, params=params) as response:
            soup = bs(await response.text(), 'html.parser')
            two_in_one = soup.select("span.temp__value.temp__value_with-unit")
            temp_now = int(two_in_one[1].get_text())
            feels_like = int(two_in_one[2].get_text())
            type_ = soup.select("div.link__condition.day-anchor")[0].get_text()
            for_10_days = soup.select('span.temp__value.temp__value_with-unit')[7:26:2]
            for_10_days = [int(x.get_text()) for x in for_10_days]

            return temp_now, feels_like, type_, for_10_days


async def get_mail_weather(name):
    async with ClientSession() as session:
        url = 'https://pogoda.mail.ru/prognoz/' + f'{name}/'
        async with session.get(url=url) as response:
            soup = bs(await response.text(), 'html.parser')
            temp_now = soup.find('div', class_="information__content__temperature").text
            temp_now = int(temp_now.strip()[-4:-1])
            two_in_one = soup.find_all('div', class_='information__content__additional__item')[:3:2]
            feels_like = int(two_in_one[0].get_text().strip()[-5:-2])
            type_ = two_in_one[1].get_text().strip()
            rain_perc = soup.find_all('div', class_='information__content__period__additional__item')[4].text
            rain_perc = int(rain_perc.strip()[:-1])
            for_10_days = soup.find_all('div', class_="day__temperature")
            for_10_days = [int(x.get_text()[:3]) for x in for_10_days]

            return temp_now, feels_like, type_, rain_perc, for_10_days


async def get_stat(city, dao, mode='default'):
    open_weather = await asyncio.create_task(get_open_weather(city))
    if not open_weather:
        return
    name, lat, lon = open_weather[:3]
    yandex_weather = await asyncio.create_task(get_yandex_weather(lat, lon))
    mail_weather = await asyncio.create_task(get_mail_weather(name))
    now_o, feels_o = open_weather[-2:]
    now_y, feels_y, type_y, d_10_y = yandex_weather
    now_m, feels_m, type_m, rain_m, d_10_m = mail_weather
    now_r = round((now_o + now_y + now_m) / 3, 1)
    feels_r = round((feels_o + feels_y + feels_m) / 3, 1)
    d_10_r = [round((x + y) / 2, 1) for x, y in zip(d_10_y, d_10_m)]

    if mode == '10_d':
        return now_r, *d_10_r

    if mode == 'default':
        return type_y, now_r, feels_r, rain_m

#asyncio.run(get_stat('голицыно'))
