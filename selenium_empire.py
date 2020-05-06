import os
import json
import time
import random
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC


def set_proxy(ip: str, port:int):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', ip)
    profile.set_preference('network.proxy.socks_port', port)
    profile.set_preference('network.proxy.socks_version', 5)
    profile.set_preference('network.proxy.socks_remote_dns', True)
    profile.update_preferences()
    return profile


def write_to_file(site_name, page_source, element_type=None, page_index=None):
    if element_type is None and page_index is None:
        file_name = '{}_{}'.format(site_name, TODAY)
    elif page_index is None:
        file_name = "{}_{}_{}".format(site_name, element_type, TODAY)
    elif element_type is None:
        file_name = "{}_{}_{}".format(site_name, TODAY, page_index)
    else:
        file_name = "{}_{}_{}_{}".format(site_name, element_type, TODAY, page_index)
    file_path = os.path.join(site_name, file_name)
    with open(file_path, 'w') as f:
        f.write(page_source)
    print('wrote', file_path, ' to file')
    logging.info('wrote {} to file'.format(file_path))


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


def random_sleep():
    sleep_time = random.random() ** 2 * 2.14
    time.sleep(sleep_time)

def write_urls_to_file(urls, dates):
    assert len(urls) == len(dates)
    with open('empire/empire_urls.csv', 'a') as f:
        for url, date in zip(urls, dates):
            f.write(",".join([url, date]))
            f.write('\n')

logging.basicConfig(filename='crawler.log',level=logging.INFO)
logging.info('[begin] Started a new round of darknet scraping.')
logging.info(get_time())


TODAY = datetime.today().strftime("%m%d%Y")

driver = webdriver.Firefox(firefox_profile=set_proxy('127.0.0.1', 9050))

dark_fail_url = 'http://darkfailllnkf4vf.onion/captcha/empire'
driver.get(dark_fail_url)

random_sleep()
# get the submit button
bt_submit = driver.find_element_by_xpath("//input[@type='submit']")
# wait for the user to click the submit button (check every 1s with a 1000s timeout)
WebDriverWait(driver, timeout=1000, poll_frequency=1) \
  .until(EC.staleness_of(bt_submit))

print("submitted")

grey_urls = driver.find_elements_by_xpath("//td[@class='url status2']")
urls = [url.text.split(' ')[0] for url in grey_urls]
black_urls = driver.find_elements_by_xpath("//td[@class='url status1']")
black_urls = [url.text for url in black_urls]
dates = [url.text.split('Online:')[1].strip() for url in grey_urls]
write_urls_to_file(urls, dates)
driver.set_page_load_timeout(20)
valid_empire_url = None
urls += black_urls
print(urls)
for url in urls:
    try:
        print(url)
        driver.get(url)
        valid_empire_url = url
        break
    except WebDriverException:
        continue

if valid_empire_url is not None:
    print('succeeded!', valid_empire_url)

user_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath("//input[@placeholder='Username']"))
user_element.send_keys('rchen')
password_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath("//input[@placeholder='Password']"))
password_element.send_keys('echo19921221')
submit_element = driver.find_element_by_xpath("//input[@type='submit']")
# wait for the user to click the submit button (check every 1s with a 1000s timeout)
WebDriverWait(driver, timeout=30, poll_frequency=1) \
  .until(EC.staleness_of(submit_element))

print('logged in')


def scraped_pages(site_name, date):
    files = os.listdir(site_name)
    pages = []
    for a_file in files:
        if date in a_file:
            page = int(a_file.split('_')[-1])
            pages.append(page)
    if len(pages) > 0:
        assert len(pages) == max(pages)
    return len(pages)

scraped_page_count = scraped_pages('empire', TODAY)
page_count = 100
driver.set_page_load_timeout(100)
for i in range(page_count - scraped_page_count):
    index = (i+scraped_page_count) * 15
    page_url = "{}/category/categories/1/{}".format(valid_empire_url, index)
    driver.get(page_url)
    write_to_file('empire', driver.page_source, page_index=i+1+scraped_page_count)
    
#logging.info('[end] finished scraping all websites')
