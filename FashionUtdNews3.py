from bs4 import BeautifulSoup
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import date, timedelta, datetime
import os
from pyairtable import Table
from urllib import parse

url = "https://fashionunited.uk/news"
newslist = []
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
currentdate = date.today()
lastdate = currentdate - timedelta(days=7)
delta = currentdate -lastdate
api_key = "keyGgWfIqVR1Ivcbx"


driver.get(url)
print("Finding news stories up to 7 dats...")
while delta.days <= 7 and delta.days >= 0:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    url = driver.current_url
    time.sleep(3)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    itemlist = soup.find_all("div", class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-lg-3 e1vq9p600 css-4cgb18")
    lastitem = itemlist[len(itemlist)-1]
    link = lastitem.find("a", class_="css-415em0 e1bxj4o80").get("href")
    datestr = link[-13:-5]
    year = datestr[0:4]
    month = datestr[4:6]
    day = datestr[-2:]
    currentdate = date(int(year),int(month),int(day))
    delta = currentdate - lastdate

soup = BeautifulSoup(page_source, "html.parser")

itemlist = soup.find_all("div", class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-lg-3 e1vq9p600 css-4cgb18")


for item in itemlist:
    headline = item.h2.text
    print(headline)
    industrytext = item.find("span", class_="MuiTypography-root MuiTypography-overline highlight-color e10wfz696 css-1t7ohnb").text.split()
    industry = industrytext[0]
    preview = item.find("p", class_="MuiTypography-root MuiTypography-body2 e10wfz694 css-hhrxas").text
    date = item.find("p", class_="MuiTypography-root MuiTypography-caption e10wfz693 css-eovdc8").text
    link = "https://fashionunited.uk" + item.find("a", class_="css-415em0 e1bxj4o80").get("href")
    driver.get(link)
    try:
        userid_element = driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div/div/article/div[1]/header/div[2]/div/div[1]/a')
        author = userid_element.text
    except:
        author = ""
    newslist.append([headline,link,industrytext,preview,date,author])
   

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
