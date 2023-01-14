import requests
import urllib
from bs4 import BeautifulSoup
import csv


URL =  "https://fashionunited.com/i/top100/"

res = requests.get(URL)

txt = res.text
status = res.status_code

soup = BeautifulSoup(res.content, "html.parser")

title = soup.title.text
head = soup.head
body = soup.body
table = soup.find("table")
tr = table.find_all("tr")

rows=[["Symbol","Name","Country","Market Cap"]]

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
    result.insert(2,alt)
    rows.append(result) 
with open("C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/top100.csv", "w") as f:
    write = csv.writer(f)
    write.writerows(rows)




