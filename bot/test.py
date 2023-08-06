# import requests
# from lxml import html
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# # proc = ['20.219.182.59', '200.111.104.59', '74.82.50.155', '201.182.251.140', '103.111.118.68', '203.150.113.98', '203.150.113.172', '154.236.191.44', '203.150.128.102', '49.49.60.46', '146.196.108.94', '116.12.44.19', '103.87.169.205', '186.121.235.66', '177.129.252.222', '95.56.254.139', '129.151.88.6', '181.191.94.126', '91.204.239.189', '202.8.74.14', '103.242.99.182', '158.101.228.50', '202.40.177.69', '64.225.8.191', '36.93.106.247', '205.233.79.250', '95.217.68.48', '45.224.22.177', '83.151.4.172', '151.22.181.211', '110.77.246.69', '45.70.200.97', '204.157.241.12', '199.243.245.94', '154.236.179.227']
# #
# # for i in range(len(proc)):
# #     try:
# #         proxies = {'https:': proc[i]}
# #         url = 'https://www.yandex.ru/pogoda/moscow'
# #         resp = requests.get(url=url,proxies=proxies)
# #         if resp.url[:33]=='https://www.yandex.ru/showcaptcha':
# #             print(i)
# #             continue
# #         with open('proxy_test.html','w',encoding='utf-8') as file:
# #             file.write(resp.text)
# #         break
# #     except Exception as r:
# #         print(r)
#
# url_for_proxy = 'http://free-proxy.cz/ru/proxylist/country/all/https/ping/all/2'
# options = Options()
# options.page_load_strategy = 'eager'
# # op = webdriver.ChromeOptions()
# # op.add_argument('headless')
# driver = webdriver.Chrome()#options=op)
# driver.get(url_for_proxy)
# tree = html.fromstring(driver.page_source)
# res = tree.xpath('//td[@class="left" and  @style="text-align:center"]/text()')
# print(res)


from datetime import datetime, timedelta

d = (datetime.today() + timedelta(days=1)).strftime('%d-%m')
td = datetime.today()
result_weather_10_days = "{} " \
                         "Сегодня: {}\n" \
                         "Завтра: {}\n" \
                         f"{(td+timedelta(days=2)).strftime('%d-%m')} {{}}°C\n" \
                         f"{(td+timedelta(days=3)).strftime('%d-%m')} {{}}°C\n"\
                         f"{(td+timedelta(days=4)).strftime('%d-%m')} {{}}°C\n"\
                         f"{(td+timedelta(days=5)).strftime('%d-%m')} {{}}°C\n"\
                         f"{(td+timedelta(days=6)).strftime('%d-%m')} {{}}°C\n"\
                         f"{(td+timedelta(days=7)).strftime('%d-%m')} {{}}°C\n"\
                         f"{(td+timedelta(days=8)).strftime('%d-%m')} {{}}°C\n"\
                         f"{(td+timedelta(days=9)).strftime('%d-%m')} {{}}°C\n"\
                         f"{(td+timedelta(days=10)).strftime('%d-%m')} {{}}°C\n"
print(result_weather_10_days)