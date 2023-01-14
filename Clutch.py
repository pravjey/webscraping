from bs4 import BeautifulSoup
import os
from pyairtable import Table
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.alert import Alert
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import sys


def extract_data(li):
        h3 = li.find("h3").text
        clutchurl = "https://clutch.co/" + li.find("a")["href"]
        orgname = h3.strip()
        img = li.find("img")
        try:
            logo = img["src"]
        except:
            logo = img["data-src"]
        div = li.find("div", class_="module-list")
        span = div.find_all("span")
        minprojsize = span[0].text
        rateperhour = span[1].text
        try:
                location = span[3].text
                location = location.split(",")
                if len(location) == 2:
                        country = location[1].strip()
                        city = location[0].strip()
                else:
                        country = location[0].strip()
                        city = ""
        except:
                country = ""
                city = ""
        #scrape about text
        driver.get(clutchurl)
        page_source1 = driver.page_source
        soup1 = BeautifulSoup(page_source1, "html.parser")
        div = soup1.find("div", id="summary_description")
        plist = div.find_all("p")
        about = ""
        for p in plist:
            about += p.text
        return [orgname,clutchurl,logo,rateperhour,minprojsize,country,city,about]

def store_data(li):
        orgtable = Table(api_key, "appRqMNg8oi3Mb0VF", "ORGANISATION")
        for row in itemlist:
            orgtable.create({
                "Organisation Name": row[0],
                "Clutch URL": row[1],
                "Logo": row[2],
                "Rate per Hour": row[3],
                "Minimum Project Size": row[4],
                "Country": row[5],
                "City": row[6],
                "About": row[7]
            })
        return
        

path = "https://clutch.co/developers/artificial-intelligence"
api_key = "keyGgWfIqVR1Ivcbx"

itemlist = []
driver = uc.Chrome()
#driver.set_page_load_timeout(600)

driver.get(path)
soup = BeautifulSoup(driver.page_source, "html.parser")
ul = soup.find("ul", class_="directory-list")

# Webscrape sponsors (page 1)

print("Webscraping page 1...")

li_list = ul.find_all("li", class_="provider provider-row sponsor") 
for li in li_list:
        print("\r",li_list.index(li))  
        itemlist.append(extract_data(li))

# Webscrape non-sponsors (page 1)

li_list = ul.find_all("li", class_="provider provider-row") 
for li in li_list:
        print("\r",li_list.index(li))
        itemlist.append(extract_data(li))

print("\n")

print(len(itemlist), " items scraped")
print("Saving Page 1 to Airtable/Organisation...")            
store_data(itemlist)

# Wenscrape remainder of pages

for i in range(2,78):
        print("Webscraping page " + str(i))
        try:
                driver.get(path + "?page=" + str(i))
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                ul = soup.find("ul", class_="directory-list")        
                li_list = ul.find_all("li", class_="provider provider-row") 
                for li in li_list:
                        print("\r",li_list.index(li))
                        itemlist.append(extract_data(li))
        except:
                continue
        print(len(itemlist), " items scraped")
        print("Saving Page",str(i),"to Airtable/Organisation...")            
        store_data(itemlist)
