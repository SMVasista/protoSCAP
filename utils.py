from __future__ import division
import sys, os, re, random, pickle
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from time import sleep
from parsel import Selector

import parameters

def kickstart_driver(driverpath, cap):
    signal = 0
    i = 1
    while signal != 1 and i < 10:
        try:
            print('trying to kickstart driver functions... TRIAL: '+str(i)) 
            driver = webdriver.Firefox(capabilities = cap, executable_path=driverpath)
            driver.get('https://www.whatismyip.com/')
            sleep(1)
            signal = 1
            driver.quit()
        except:
            sleep(1)
            i += 1
            pass
    return signal
        

def login_into_linkedIn(driverpath, cap):
    # Default login parameters
    login_uname = parameters.linkedIn_login['uname']
    login_passwd = parameters.linkedIn_login['passwd']

    # specifies the path to the chromedriver.exe
    driver = webdriver.Firefox(capabilities = cap, executable_path=driverpath)

    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://www.linkedin.com/uas/login')

    # locate email form by_class_name
    username = driver.find_element_by_id('username').send_keys(login_uname)

    # sleep for 0.5 seconds
    sleep(1)

    # locate password form by_class_name
    password = driver.find_element_by_id('password').send_keys(login_passwd)

    sleep(1)

    # locate submit button by_xpath
    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

    # .click() to mimic button click
    sign_in_button.click()

    return driver


def validate_linkedIn_URL(url):
    strg = str(url)
    if 'https://www.linkedin.com/' in strg or 'linkedin.com/' in strg:
        return 0
    else:
        return 1

if __name__=="__main__":
    pass
