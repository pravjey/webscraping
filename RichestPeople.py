import requests
import urllib
from bs4 import BeautifulSoup
import csv


URL =  "https://fashionunited.com/i/richest-people-in-fashion/"

res = requests.get(URL)

txt = res.text
status = res.status_code

soup = BeautifulSoup(res.content, "html.parser")

title = soup.title.text
head = soup.head
body = soup.body
table = soup.find("table")
tr = table.find_all("tr")

rows=[["Name","Company","Net worth 2015","Net worth 2016","Net worth 2017","Index ranking","Country"]]

file = open("C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/countrycodes.csv", "r")
csv_reader = csv.reader(file)
countrycodes = []
for row in csv_reader:
    countrycodes.append(row)

for e in tr[1:]:
    result = e.text.strip()
    image = e.find("amp-img")
    alt = image.get("alt")
    alt = alt[(len(alt)-2):]
    for i in countrycodes:
        if alt == i[3].lower():
            alt = i[0]
            break
    result = result.split('\n')
    while '' in result:
        result.remove('')
    index = result[0]
    result.insert(6,result[0])
    result.remove(result[0])
    result.append(alt)
    rows.append(result)
    
with open("C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/RichestPeople.csv", "w") as f:
    write = csv.writer(f)
    write.writerows(rows)
