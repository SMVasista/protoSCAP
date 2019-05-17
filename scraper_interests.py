from __future__ import division
import sys, os, re, random, pickle
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from time import sleep
from parsel import Selector
import datetime
now = datetime.datetime.now()
curr_year = int(now.year)
import parameters
import utils

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
    cap = {"marionette": True}
    
    driver = utils.login_into_linkedIn(driverpath, cap)

    for url in urls:
        HOLDER[url] = []
        #driver = webdriver.Firefox(capabilities = cap, executable_path=driverpath)
        driver.get(url)
        driver.execute_script("window.scrollTo(0, 200)")
        sleep(1)
        driver.execute_script("window.scrollTo(0, 400)")
        sleep(1)
        driver.execute_script("window.scrollTo(0, 600)")
        sleep(1)
        driver.execute_script("window.scrollTo(0, 1000)")
        sleep(1)
        driver.execute_script("window.scrollTo(0, 3000)")
        sleep(1)
        driver.execute_script("window.scrollTo(0, 5000)")
        sleep(1)
        driver.execute_script("window.scrollTo(0, 7000)")
        # add a 5 second pause loading each URL
        sleep(2 + random.randint(0, 2))
        html = unicode(driver.page_source.encode("utf-8"), "utf-8")
        data = soup(html, 'html.parser')
        m = data.findAll("p", {"class", "pv-entity__dates t-14 t-black--light t-normal"})
        try:
            dates = []
            for elem in m[0].findAll("time"):
                dates.append(int(elem.get_text()))
            #Assuming an average individual graduates by the age of 22
            print dates
            age = (curr_year - dates[-1]) + 22
        except:
            age = 'NA'
        d = data.findAll("span", {"class", "pv-entity__summary-title-text"})
        for elem in d:
            try:
                HOLDER[url].append(elem.get_text())
            except:
                pass
        HOLDER[url].append(('age', age))
        # add a 5 second pause loading each URL
        sleep(5 + random.randint(1, 3))

        print age
        print HOLDER

    driver.quit()

    return HOLDER

if __name__=="__main__":
    pass
