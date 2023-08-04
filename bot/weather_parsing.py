import asyncio
import time
from aiohttp import ClientSession


async def get_openweather(city):
    async with ClientSession() as session:
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56', 'units':'metric'}

        async with session.get(url=url, params=params) as response:
            weather = await response.json()
            if weather.get('message'):
                return
            return weather['coord']['lat'], weather['coord']['lon'], weather['weather'][0]['main'], \
                weather['main']['temp'], weather['main']['feels_like']



async def get_stat(city):
    open_weather = await asyncio.create_task(get_openweather(city))
    return open_weather

#asyncio.run(get_stat('голицыно'))
