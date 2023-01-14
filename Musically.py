import requests
import urllib
from bs4 import BeautifulSoup
import csv
import json
import os
from pyairtable import Table
import datetime


path = "https://musically.com/news/page/"
page = 1
currentdate = datetime.date.today()
lastdate = currentdate - datetime.timedelta(days=7)
delta = currentdate - lastdate
newslist = []
api_key = "keyGgWfIqVR1Ivcbx"

while delta.days <= 7 and delta.days >= 0:
    print("Webscraping page ",str(page))
    url = path + str(page) + "/"
    res = requests.get(url)

    soup = BeautifulSoup(res.content, "html.parser")

    articles = soup.find_all("a", class_="article_inner")

    for article in articles:
        date = article.find("div", class_="article_date_container").text
        date = date[1:]
        date_elements = date.split(" ")[0:3]
        date_elements[1] = date_elements[1][0:(len(date_elements[1])-1)]
        date_elements[0] = datetime.datetime.strptime(date_elements[0], "%B")
        date_elements[0] = date_elements[0].month
        currentdate = datetime.date(int(date_elements[2]),int(date_elements[0]),int(date_elements[1]))
        delta = currentdate - lastdate
        if delta.days <= 7 and delta.days >= 0:
            link = article["href"]
            headline = article.find("div", class_="article_title").text
            preview = article.find("div", class_="article_excerpt").text
            res1 = requests.get(link)
            soup1 = BeautifulSoup(res1.content, "html.parser")
            author = soup1.find("div", id="entry_author").text
            author = author[12:]
            newslist.append([headline,link,preview,date,author])
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






