from __future__ import division
import sys, os, re, random, pickle
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from time import sleep
import parameters
#import requests
from parsel import Selector

# function to ensure all key data fields have a value
def validate_field(field):# if field is present pass if field:pass
    if field != None:
        return field
    else:
        return 'NR'

def execute(urls):
    HOLDER = {}
    # Configuring Firefox driver (geckodriver)
    cwl = os.getcwd()
    driverpath = str(os.path.join(cwl, 'geckodriver'))
    cap = {}
    cap["marionette"] = True

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
    sleep(2)

    # locate password form by_class_name
    password = driver.find_element_by_id('password').send_keys(login_passwd)

    sleep(1)

    # locate submit button by_xpath
    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

    # .click() to mimic button click
    sign_in_button.click()

    for url in urls:
        HOLDER[url] = []
        #driver = webdriver.Firefox(capabilities = cap, executable_path=driverpath)
        driver.get(url)
        driver.execute_script("window.scrollTo(0, 7500)")
        
        # add a 5 second pause loading each URL
        sleep(2 + random.randint(0, 2))
        html = unicode(driver.page_source.encode("utf-8"), "utf-8")
        data = soup(html, 'html.parser')
        d = data.findAll("span", {"class", "pv-entity__summary-title-text"})
        for elem in d:
            try:
                HOLDER['url'].append(elem.get_text())
            except:
                pass
        # add a 5 second pause loading each URL
        print 'Waiting'
        sleep(5 + random.randint(1, 3))

    return HOLDER

if __name__=="__main__":
    pass
