from mailbox import NotEmptyError
from queue import Empty
import warnings
warnings.filterwarnings("ignore")
from selenium import webdriver
import streamlit as st
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as soup
import pandas as pd
import csv
import re

st.set_page_config(page_title="Rise - Job Search", page_icon=":mag:", layout="wide")
driver = webdriver.Chrome(executable_path="chromedriver.exe")



def search(sear,loc):
    naukriurl= f'https://www.naukri.com/{sear.replace(" ", "-")}-jobs-in-{location.replace(" ", "+")}'
    filename = f"{sear} jobs in {location} naukri.csv"
    seen=set()
    lists = []
    l = {}
    with open(filename, "w", newline='') as myfile:
        spamWriter = csv.writer(myfile, dialect='excel')
        spamWriter.writerow(["Job Title","Company", "Experience", "Location","Salary","Link", "Skills"]) 
        naukriurls = [naukriurl, naukriurl + "-2", naukriurl + "-3", naukriurl + "-4"]
        for naukriurl in naukriurls:
            try:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--incognito")
                chrome_options.add_argument("--headless")
                #driver = webdriver.Chrome(executable_path="C:\chromedriver.exe")
            except:
                #binary: str = r'C:\Program Files\Mozilla Firefox\firefox.exe'
                #options = Options()
                #options.set_headless(headless=True)
                #options.binary = binary
                #cap = DesiredCapabilities().FIREFOX
                #cap["marionette"] = True
                #driver = webdriver.Firefox(firefox_options=options, capabilities=cap, executable_path="geckodriver.exe")'''
                pass
            
            driver.get(naukriurl)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            src = driver.page_source
            driver.close()
            page_soup = soup(src, "lxml")
            print(naukriurl)

            containers = page_soup.findAll("article",  {"class": "jobTuple bgWhite br4 mb-8"})
            for container in containers:
                name_container1 = container.find("a", {"class": "title"})
                link = name_container1.get('href')
                jobtitle = name_container1.text
                cycontainer = container.find("div", {"class": "companyInfo"})
                cy=cycontainer.find("a")
                com = cy.text
                experience = container.find("li", {"class": "fleft grey-text br2 placeHolderLi experience"})
                exp = experience.find("span") #, {"class" : "ellipsis fleft fs12 lh16 expwdth"}
                #expe = exp.text
                #exp = expe[54:]
                loc = container.find("li", {"class": "location"})
                locs=loc.find("span")
                loc=locs.text
                salary = container.find("li", {"class": "salary"})
                sal= salary.find("span")
                salary=sal.text
                skills_container = container.findAll("li", {"class": "fleft fs12 grey-text lh16 dot"})
                #skills = skills_container.text
                skills = ', '.join([item.text for item in skills_container])
                l=[str(str(jobtitle).strip()), str(str(com.strip())),  str(str(exp).strip()), str(str(loc).strip()), str(str(salary).strip()),
                    f'=HYPERLINK("{str(str(link).strip())}")', str(str(skills).strip())] #'''str(str(exp).strip())''',
                lists.append(l)
                if l[1] not in seen:
                    spamWriter.writerow(l)
                    seen.add(l[1])
        
            lists = pd.DataFrame(lists)
            lists.columns = ["Job Title","Company", "Experience", "Location","Salary","Link", "Skills"]
            #lists["Experience"] = lists["Experience"].apply(lambda text: (re.search('Yrs ">(.*)</span>', text)).group(1))
            #print(lists[2].head())
            
            from subprocess import Popen
            p = Popen(filename, shell=True)
        st.dataframe(lists)
        st.download_button("Download", lists.to_csv(), mime='text/csv')

        #st.button("Analyse the results!", analyse(lists))



csv.register_dialect('escaped', escapechar='\\', doublequote=True, quoting=csv.QUOTE_ALL)
sear=st.text_input("What type of job are you looking for?")
location=st.text_input("What location do you want to search around?" )
if sear is not None:
    search(sear,location)
