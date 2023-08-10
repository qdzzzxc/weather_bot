from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def update_proxies():
    final_res = []
    url_for_proxy = 'http://free-proxy.cz/ru/proxylist/country/all/https/ping/all'
    options = Options()
    options.page_load_strategy = 'eager'
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome()
    driver.get(url_for_proxy)
    tree = html.fromstring(driver.page_source)
    ip = tree.xpath('//td[@class="left" and  @style="text-align:center"]/text()')
    port = tree.xpath('//span[@class="fport"]/text()')
    final_res = [f'HTTPS://{x}:{y}' for x, y in zip(ip, port)]
    with open('proxies.txt','w') as file:
        for line in final_res:
            file.write(f"{line}\n")

update_proxies()