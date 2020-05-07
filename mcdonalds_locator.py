import os
import json
import time
import random
import re
import math
import pandas as pd
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains



def read_zip_codes():
    df = pd.read_csv('data/zip_codes_in_the_world.csv')
    zip_codes = list(set(df['zip_code']))
    return zip_codes

zip_code_list = read_zip_codes()

def get_zip_code():
    if len(zip_code_list) == 0:
        print('looped through all the zip codes')
        return False
    zip_code = random.choice(zip_code_list)
    zip_code_list.remove(zip_code)
    return zip_code

def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def random_sleep():
    sleep_time = random.random() * 2
    time.sleep(sleep_time)

logging.basicConfig(filename='crawler.log',level=logging.INFO)
logging.info('[begin] Started a new round of scraping.')
logging.info(get_time())

TODAY = datetime.today().strftime("%m%d%Y")

target_zip_code = get_zip_code()
print('search zip code: {}'.format(target_zip_code))
if target_zip_code:
    driver = webdriver.Firefox()
    locator_url = 'https://www.mcdonalds.com/us/en-us/restaurant-locator.html'
    driver.get(locator_url)
    zip_code_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath("//input[@id='search']"))
    zip_code_element.send_keys(target_zip_code)
    search_button = driver.find_element_by_xpath("//button[@type='submit']")
    search_button.click()
    list_view_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='toggleListMapView()']")))
    list_view_button.click()

    count_element = driver.find_element_by_xpath("//div[@class='mcd-rlresults__filters__heading ng-binding']")
    store_count_list = re.findall(r'\d+', count_element.text)
    store_count = list(map(int, store_count_list))[0]
    print('this search found {} stores'.format(store_count))
    click_count = math.ceil(float(max(store_count-5.0, 0)) / 5.0)
    if click_count > 0:
        for _ in range(click_count):
            load_more_flag = driver.find_element_by_xpath("//button[@ng-click='toggleTotalVisibleRestaurants()']")
            print('load more flag:', load_more_flag)
            if load_more_flag:
                random_sleep()
                actions = ActionChains(driver)
                #menu_element = driver.find_element_by_xpath("//p[@id='alert-box-message']")
                #actions.move_to_element(menu_element)
                load_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='toggleTotalVisibleRestaurants()']")))
                actions.move_to_element(load_more_button)
                actions.click(load_more_button)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                actions.perform()
                random_sleep()
            else:
                break
    print("successful!!!!")
