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

rows=[]

file = open("C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/countrycodes.csv", "r")
csv_reader = csv.reader(file)
countrycodes = []
for row in csv_reader:
    countrycodes.append(row)

for e in tr[1:]:
    result = e.text.strip()
    result = result.split('\n')
    while '' in result:
        result.remove('')
    result.remove(result[0])
    result.insert(0,len(rows)+1)
    rows.append(result)




with open("C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/MostValuable.csv", "w") as f:
    write = csv.writer(f)
    write.writerows(rows)




