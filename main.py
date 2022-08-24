# -*- coding: utf-8 -*-
import json
import os
from dotenv import load_dotenv


import time

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import select
from selenium.webdriver.support.ui import WebDriverWait

from mail import send_email
# Load environment variables from .env file
load_dotenv()


def auto_temp():
    email = f"{os.environ.get('USERNAME')}@u.nus.edu"
    pw = os.environ.get("PASSWD")

    CHROMEDRIVER_PATH = "chromedriver"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--incognito')
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('start-maximized')
    # chrome_options.add_argument('disable-infobars')
    # chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_bin = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
    # chrome_options.binary_location = chrome_bin
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

    # Navigate to Microsoft login page
    print("Starting auto_temp()...")
    driver.get('https://bit.ly/WeeklyHD_NOC')
    time.sleep(10)
    # Login phase
    email_input = driver.find_element_by_name('loginfmt')
    email_input.send_keys(email)
    time.sleep(0.5)
    
    # Navigate to NUS login page

    driver.find_element_by_id("idSIButton9").click()
    print("Navigating to NUS login page...")
    time.sleep(10)

    # ARCHIVED: Uncomment to debug
    # html = driver.execute_script("return document.body.outerHTML;")
    # print(html)
    # time.sleep(10)

    # Enter password
    password_input = driver.find_element_by_id('passwordInput')
    password_input.send_keys(pw)

    # Navigate to stay signed in page
    driver.find_element_by_id("submitButton").click()
    print("Navigating to stay signed in page...")
    time.sleep(10)

    # Navigate to form response page
    driver.find_element_by_id("idBtn_Back").click()
    print("Navigating to form response page...")
    time.sleep(10)

    # Select appropriate options
    driver.find_element_by_css_selector("[name='r7e5877b3cce7458b82eb0b9b2960eae2'][value='No']").click()
    driver.find_element_by_css_selector("[name='r2db3230d15a14a62b9919d992340dcfa'][value='No']").click()
    driver.find_element_by_css_selector("[name='r830048074c1a423fbdb242cce016b629'][value='No']").click()
    driver.find_element_by_css_selector("[type='checkbox']").click()
    print("Filled ALL options!")
    time.sleep(0.5)
    

    driver.find_element_by_class_name("office-form-bottom-button").click()

    print("COMPLETED!")
    time.sleep(10)

    #exit
    driver.quit()    

def handle_stale(func):
    '''Used to rerun specific function for 5 times if element has gone stale / cannot be found'''
    isStale = True
    while isStale:
        i = 1
        try:
            func()
            isStale = False
        except Exception as e:
            i+=1
            print(f"Failed to declare / record temperature!, {e}")
            print(f"Retrying... Attempt {i}")
            if i >= 5:
                print(f"Failed to declare / record temperature!, {e}. Attempt {i}")
                send_email(isSuccessful=False)
                isStale = False
    
def declare():
    handle_stale(auto_temp)
    send_email()


if __name__ == "__main__":
    declare()
