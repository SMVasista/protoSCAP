from __future__ import division
import sys, os, re, pickle
###############################################################################
import scraper_basic as sb
import scraper_interests as sc
import stencils
import utils
import cluster
import parameters
###############################################################################
###############################################################################

strg = []

def executeSCAP(urls):
    #Initiating scraping program. Check existing data before.
    if len(urls) < 1:
        exit(0)

    #Try loading scraped data stored as scraped_data_dump
    try:
        with open('scraped_data_dump', 'r') as f:
            dump = pickle.load(f)
        url_logs = dump[0]
        S = dump[1]
    except:
        url_logs = []
        S = {}
        strg.append('source data dump not found...\n')

    #Checking datalogs
    parsed_url = []
    scraped_url = []
    
    for url in urls:
        if url in url_logs:
            scraped_url.append(url)
        else:
            parsed_url.append(url)

    if len(parsed_url) > 0:
        
        print(str(len(parsed_url))+'/'+str(len(urls))+' new URLs found for scraping')
        ###################################################
        cwl = os.getcwd()
        driverpath = str(os.path.join(cwl, 'geckodriver'))
        cap = {"marionette": True}
        utils.kickstart_driver(driverpath, cap)
        ###################################################

        #strg.append(str(p_url)+' Extracting basic details.\n')
        #Executing basic scrape
        try:
        #if True:
            H = sb.execute(parsed_url)
        except:
            #strg.append(str(p_url)+' could not be parsed.\n')
            H = ['NA1']
            pass

        #strg.append(str(p_url)+' Extracting Interests & connections.\n')
        #Executing interests scrape
        try:
            I = sc.execute(parsed_url)
        except:
            #strg.append(str(p_url)+' could not be parsed.\n')
            I = ['NA2']
            pass
        
        try:
            for element in H.keys():
                S[element] = (H[element], I[element])
                url_logs.append(element)
        except:
            #strg.append(str(p_url)+' could not be appended to dump - incomplete data.\n')
            pass

        H = {}
        I = {}
        for s_url in scraped_url:
            print(str(len(scraped_url))+'/'+str(len(urls))+' exisitng URLs found in database')
            H[s_url] = S[s_url][0]
            I[s_url] = S[s_url][1]
            
        #Updating database with information
        #for url
    else:
        print(str(len(scraped_url))+'/'+str(len(urls))+' exisitng URLs found in database')
        H = {}
        I = {}
        for s_url in scraped_url:
            H[s_url] = S[s_url][0]
            I[s_url] = S[s_url][1]

    #Storing back scraped data
    with open('scraped_data_dump', 'w') as f:
        dump = pickle.dump((url_logs, S), f)

    for element in H:
        print H[element]['Name']
    
    #Logging error statements before exiting
    #@pl.updateLog(os.path.join(cwl, logFileName), strg)
    return H, I

def executeCMapper(H, I):
    #Passing data into stencils
    H_ = {}
    I_ = {}
    for element in H.keys():
        if len(H[element]) != 0 and len(I[element]) != 0:
            H_[element] = stencils.parse_basic_details(H[element])
            I_[element] = stencils.parse_interests_details(I[element])
        Mx, Dmx = stencils.generate_vo_matrix(H_, I_)
    return Mx, Dmx

def executeCVF(Mx, Dmx):
    Clusters = cluster.identifyClusters(Mx, Dmx)

if __name__=="__main__":
    pass
