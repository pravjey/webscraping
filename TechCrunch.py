from bs4 import BeautifulSoup
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
import time
from time import strptime
from datetime import date, timedelta, datetime
import os
from pyairtable import Table
from urllib import parse

url = "https://techcrunch.com/"
newslist = []
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
currentdate = date.today()
lastdate = currentdate - timedelta(days=7)
delta = currentdate -lastdate
api_key = "keyGgWfIqVR1Ivcbx"


driver.get(url)
driver.implicitly_wait(10)
button = driver.find_element(by=By.XPATH, value='//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button')
button.click()
print("Finding news stories up to 7 dats...")
page=1

while delta.days <= 7 and delta.days >= 0:
    print("Loading page", page)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    url = driver.current_url
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    itemlist = soup.find_all("time", class_="river-byline__full-date-time")
    lastitem = itemlist[len(itemlist)-1]
    item = lastitem.text
    datestr = item[14:]
    date_elements = datestr.split(" ")
    year = date_elements[2]
    month_name = date_elements[0]
    if ord(month_name[0]) < 65 or ord(month_name[0]) > 122:
        month_name = month_name[1:]
    month = strptime(month_name, "%B").tm_mon
    day = date_elements[1][0:len(date_elements[1])-1]
    currentdate = date(int(year),int(month),int(day))
    delta = currentdate - lastdate
    button1 = driver.find_element(by=By.XPATH, value='//*[@id="tc-main-content"]/div[3]/div/div/button')
    try:
        button1.click()
    except:
        continue
    page += 1

soup = BeautifulSoup(page_source, "html.parser")

itemlist = soup.find_all("article")

for item in itemlist:
    print(item)
    skip = False
    try:
        headline = item.find("h3") or item.find("h2")
    except:
        skip = True
    if not skip:
        print(headline)
        headlinetext = headline.text
        print(headlinetext)
        a = headline.find("a")
        link = url[0:22] + a["href"]
        print(link)
        author = item.find("p").text
        print(author)
        date = item.find("time", class_="river-byline__full-date-time")
        print(date)
        #newslist.append([headlinetext,link,preview,date,author])


   
"""

print("Saving to Airtable/News...")            
newstable = Table(api_key, "appRqMNg8oi3Mb0VF", "NEWS")

for row in newslist:
    newstable.create({
        "HEADLINE": row[0],
        "Date Published": row[4],
        "PREVIEW": row[3],
        "Author.": row[5],
        "Article Link": row[1]
    })

print("Saved", len(newslist), "news stories.")
"""
