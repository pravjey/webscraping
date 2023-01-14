import requests
import urllib
from bs4 import BeautifulSoup
import csv
import json
import os
from pyairtable import Table
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


url = "https://musictech.com"
path = "/news/page/"
page = 1
currentdate = datetime.date.today()
lastdate = currentdate - datetime.timedelta(days=7)
delta = currentdate - lastdate
newslist = []
api_key = "keyGgWfIqVR1Ivcbx"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

while delta.days <= 7 and delta.days >= 0:
    print("Webscraping page ",str(page))
    if page > 1:
        newsmenu_link = url + path + str(page) + "/"
    else:
        newsmenu_link = url + "/news"
    #print(newsmenu_link)
    driver.get(newsmenu_link)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")

    articles1 = soup.find_all("div", class_="bg-black transition duration-500 transform hover:-translate-y-2 hover:shadow-lg css-1d7cmgr")
    articles2 = soup.find_all("div", class_="bg-black transition duration-500 transform hover:-translate-y-2 hover:shadow-lg css-1vuem7b")
    articleslist = [articles1, articles2]
    
    for i in articleslist:
        for article in i:
            block = article.find("div", class_="max-w-md p-5")
            dateblock = block.find("div", class_="mt-4 sm:mt-5 text-right text-white font-info text-sm")
            date = dateblock.find("div")["title"]
            date = date[9:]
            date = date[:-7]
            date_elements = date.split(" ")[1:]
            date_elements[1] = date_elements[1][0:(len(date_elements[1])-1)]
            date_elements[0] = datetime.datetime.strptime(date_elements[0], "%B")
            date_elements[0] = date_elements[0].month
            currentdate = datetime.date(int(date_elements[2]),int(date_elements[0]),int(date_elements[1]))
            delta = currentdate - lastdate
            if delta.days <= 7 and delta.days >= 0:
                a = block.find("a")
                newspage_link = url + a["href"]
                #print(newspage_link)
                headline = a.text
                res1 = requests.get(newspage_link)
                soup1 = BeautifulSoup(res1.content, "html.parser")
                author = soup1.find("a", class_="font-bold hover:opacity-70 text-link").text
                preview = soup1.find("div", class_="post-subtitle mb-5").text
                newslist.append([headline,newspage_link,preview,date,author])
                print(headline)
            else:
                break
    page += 1

        
    
print("Saving to Airtable/News...")            
newstable = Table(api_key, "appRqMNg8oi3Mb0VF", "NEWS")

for row in newslist:
    newstable.create({
        "HEADLINE": row[0],
        "Date Published": row[3],
        "PREVIEW": row[2],
        "Author.": row[4],
        "Article Link": row[1]
    })

print("Saved", len(newslist), "news stories.")






