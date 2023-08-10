import asyncio
import sys

from aiogram.client.session import aiohttp
from aiohttp import ClientSession, ClientProxyConnectionError, ClientConnectorSSLError
from bs4 import BeautifulSoup as bs


async def try_yandex_weather(lat, lon, proxy):
    async with ClientSession() as session:
        url = 'https://yandex.ru/pogoda/'
        params = {'lat': lat, 'lon': lon}
        try:
            async with session.get(url=url, params=params, proxy=proxy) as response:
                print(response.url)
                assert not str(response.url).startswith('https://yandex.ru/showcaptcha')
                soup = bs(await response.text(), 'html.parser')
                two_in_one = soup.select("span.temp__value.temp__value_with-unit")
                temp_now = int(two_in_one[1].get_text())
                feels_like = int(two_in_one[2].get_text())
                type_ = soup.select("div.link__condition.day-anchor")[0].get_text()
                for_10_days = soup.select('span.temp__value.temp__value_with-unit')[7:26:2]
                for_10_days = [int(x.get_text()) for x in for_10_days]

                print('вроде всё')
                return temp_now, feels_like, type_, for_10_days
        except AssertionError:
            return None
        except (ClientProxyConnectionError, ClientConnectorSSLError):
            print('следующий прокси')
            return None



async def get_weather_yandex():
    lat = 55.79612732
    lon = 49.10641479

    with open('proxies.txt', 'r') as file:
        proxies = file.read().splitlines()

    result = await try_yandex_weather(lat, lon, None)
    if result is not None:
        print(result)
        return result

    proxies = ['https://121.230.210.80:8089']
    for proxy in proxies:
        print(proxy.lower())
        result = await try_yandex_weather(lat, lon, proxy.lower())
        if result is not None:
            break

    print(result)
    return result

asyncio.run(get_weather_yandex())
