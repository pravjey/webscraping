import requests
import urllib
from bs4 import BeautifulSoup
import csv


URL =  "https://fashionunited.com/i/twitter-fashion-index/"

res = requests.get(URL)

txt = res.text
status = res.status_code

soup = BeautifulSoup(res.content, "html.parser")

table = soup.tbody

companies = table.find_all("div", class_="fu-list-link")
likes = table.find_all("div", class_="fu-list-cell")

results = [["Company","Twitter","Twitter Followers"]]

for e in range(len(companies)):
    company = companies[e].text.strip()
    twitter = companies[e].a["href"].strip()
    twitterFollowers = likes[e].text.strip()
    results.append([company,twitter,twitterFollowers])

with open("C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/Twitter.csv", "w") as f:
    write = csv.writer(f)
    write.writerows(results)




