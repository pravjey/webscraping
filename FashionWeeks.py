import requests
import urllib
from bs4 import BeautifulSoup
import csv
import re


URL =  "https://fashionunited.com/landing/fashionweeks-around-the-world-list/"

res = requests.get(URL)

txt = res.text
status = res.status_code

soup = BeautifulSoup(res.content, "html.parser")

article = soup.article
h2 = article.find_all("h2")
ul = article.find_all("ul")

h2.remove(h2[len(h2)-1])
h2.remove(h2[3])

results = [["Name", "Country", "Link"]]

for i in range(len(h2)):
    country = h2[i].text.strip()
    print("Webscraping data for ", country)
    a = ul[i].find_all("a")
    for j in a:
        name = j.text.strip()
        website = j["href"]
        results.append([name,country,website])

with open("C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/FashionWeeks.csv", "w") as f:
    write = csv.writer(f)
    write.writerows(results)
