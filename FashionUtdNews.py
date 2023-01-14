import requests
import urllib
from bs4 import BeautifulSoup
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

url = "https://fashionunited.uk/news"
newstable = []
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(url)
time.sleep(2)
scroll_pause_time = 0.2
screen_height = driver.execute_script("return window.screen.height;")
i = 1

while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    itemlist = soup.find_all("div", class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-lg-3 e1vq9p600 css-4cgb18")


    for item in itemlist:
        headline = item.h2.text
        industrytext = item.find("span", class_="MuiTypography-root MuiTypography-overline highlight-color e10wfz696 css-1t7ohnb").text.split()
        industry = industrytext[0]
        preview = item.find("p", class_="MuiTypography-root MuiTypography-body2 e10wfz694 css-hhrxas").text
        date = item.find("p", class_="MuiTypography-root MuiTypography-caption e10wfz693 css-eovdc8").text
        link = "https://fashionunited.uk" + item.find("a", class_="css-415em0 e1bxj4o80").get("href")
        driver.get(link)
        userid_element = driver.find_element(by=By.XPATH, value='//*[@id="__next"]/main/div/div/article/div[1]/header/div[2]/div/div[1]/a')
        author = userid_element.text
        newstable.append([headline,link,industrytext,preview,date,author])

    if (screen_height) * i > scroll_height:
        break


with open("C:/Users/User/Documents/Freelance work/Media and Entertainment Innovation/Airtable/Fashionutdnews.csv", "w", encoding="utf-8") as f:
    write = csv.writer(f)
    write.writerows(newstable)





