from __future__ import division
import sys, os, re, random, pickle
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from time import sleep
from parsel import Selector

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
    
    #Parsing links after logging in Linked-In
    for url in urls:
        try:
            HOLDER[url] = {'Name': None, 'Job Title': None, 'Company': None, 'College': None, 'Location': None, 'N_Connections': None}

            # get the profile URL 
            driver.get(url)

           # add a 5 second pause loading each URL
            sleep(3 + random.randint(1, 4))

           # assigning the source code for the webpage to variable sel
            sel = Selector(text=driver.page_source)

           # xpath to extract the text from the class containing the name
            name = sel.xpath('//*[starts-with(@class, "pv-top-card-section__name")]/text()').extract_first()

            if name:
                name = name.strip()


            # xpath to extract the text from the class containing the job title
            job_title = sel.xpath('//*[starts-with(@class, "pv-top-card-section__headline")]/text()').extract_first()

            if job_title:
                job_title = job_title.strip()


            # xpath to extract the text from the class containing the company
            college = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name pv-top-card-v2-section__school-name text-align-left ml2 t-14 t-black t-bold full-width ember-view")]//*[starts-with(@class, "lt-line-clamp__line lt-line-clamp__line--last")]/text()').extract_first()

            if college:
                college = college.strip()


            # xpath to extract the text from the class containing the college
            company = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name pv-top-card-v2-section__company-name text-align-left ml2 t-14 t-black t-bold full-width ember-view")]//*[starts-with(@class, "lt-line-clamp__line lt-line-clamp__line--last")]/text()').extract_first()

            if company:
                company = company.strip()


            # xpath to extract the text from the class containing the location
            location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()

            if location:
                location = location.strip()

            # xpath to extract connections of the profile
            connections = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name pv-top-card-v2-section__connections ml2 t-14 t-black t-normal")]/text()').extract_first()
            
            if connections:
                if '(' in str(connections):
                    connections = connections.split('(')[1].split(')')[0]
                elif '+' in str(connections):
                    connections = int(str(connections).split(' ')[10].split('+')[0])
                else:
                    connections = int(str(connections).split(' ')[10])

            # terminates the application
            #driver.quit()

            # validating if the fields exist on the profile
            name = validate_field(name)
            job_title = validate_field(job_title)
            company = validate_field(company)
            college = validate_field(college)
            location = validate_field(location)
            url = validate_field(url)
            connections = validate_field(connections)

            # printing the output to the terminal
            print('\n')
            print('Name: ', name)
            HOLDER[url]['Name'] = name
            print('Job Title: ', job_title)
            HOLDER[url]['Job Title'] = job_title
            print('Company: ', company)
            HOLDER[url]['Company'] = company
            print('College: ', college)
            HOLDER[url]['College'] = college
            print('Location: ', location)
            HOLDER[url]['Location'] = location
            print('Connections: ', connections)
            HOLDER[url]['N_Connections'] = connections
            print('URL: ', url)
            print('\n')
            
        except:
            print('Skipping' + str(url))
            continue

       # add a 5 second pause loading each URL
        sleep(5 + random.randint(1, 3))

    driver.quit()
    return HOLDER

if __name__=="__main__":
    pass


    
