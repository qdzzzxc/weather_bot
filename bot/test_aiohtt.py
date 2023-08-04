import asyncio
import sys

from arsenic import get_session, keys, browsers, services

if sys.platform.startswith('win'):
    GECKODRIVER = './geckodriver.exe'
else:
    GECKODRIVER = './geckodriver'


async def hello_world(name):
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    async with get_session(service, browser) as session:
        await session.get('https://www.yandex.ru/pogoda/')
        search_box = await session.wait_for_element(5, 'input[class="mini-suggest-form__input mini-suggest__input"]')
        await search_box.send_keys(name)
        await search_box.send_keys(keys.ENTER)
        await asyncio.sleep(5)
        res = await session.get_page_source()


def main(name):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hello_world(name))


if __name__ == '__main__':
    main('Голицыно')