# import asyncio
# import sys
#
# from aiohttp import ClientSession
# from bs4 import BeautifulSoup as bs
#
#
# async def get_mail_weather(name):
#     async with ClientSession() as session:
#         url = 'https://pogoda.mail.ru/prognoz/' + f'{name}/'
#         async with session.get(url=url) as response:
#             soup = bs(await response.text(), 'html.parser')
#             temp_now = soup.find('div', class_="information__content__temperature").text
#             temp_now = int(temp_now.strip()[-4:-1])
#             two_in_one = soup.find_all('div', class_='information__content__additional__item')[:3:2]
#             feels_like = int(two_in_one[0].get_text().strip()[-5:-2])
#             type_ = two_in_one[1].get_text().strip()
#             rain_perc = soup.find_all('div', class_='information__content__period__additional__item')[4].text
#             rain_perc = int(rain_perc.strip()[:-1])
#             for_10_days = soup.find_all('div', class_="day__temperature")
#             for_10_days = [int(x.get_text()[:3]) for x in for_10_days]
#
#             return temp_now, feels_like, type_, rain_perc, for_10_days
#
#
# async def main(name):
#     loop = await asyncio.create_task(get_mail_weather(name))
#     print(loop)
#
#
# asyncio.run(main('moskva'))

from transliterate import translit
ru_text = 'Часцы'
text = translit(ru_text, language_code='ru', reversed=True)
print(text)