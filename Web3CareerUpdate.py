import requests
import urllib
from bs4 import BeautifulSoup
import csv
import json

path = "https://web3.career/?page="
lastpage = 666
jobstable = []

for i in range(1,3):
    print("Webscraping page ",str(i))
    url = path + str(i)
    res = requests.get(url)

    soup = BeautifulSoup(res.content, "html.parser")

    tbody = soup.tbody
    rows = tbody.find_all("tr", class_="table_row")

    for row in rows:
        time = row.find("td", class_="align-middle job-time-ago-mobile").text.strip()
        if time[len(time)-1] == "h":
            role = row.h2.text.strip()
            org = row.h3.text.strip()
            salary = row.p.text.strip()
            location = row.find("td", class_="job-location-mobile").text.strip()
            badges = row.find("td", class_="align-middle d-none d-md-table-cell")
            badges = badges.find_all("span", class_="my-badge my-badge-secondary")
            badgeslist = []
            for i in badges:
                a = i.find("a")
                href = a.get("href")
                start = href.find("/")
                end = href.find("-jobs")
                badge = href[start:end]
                badge = badge[1:]
                badge = badge.replace("-", " ")
                badgeslist.append(badge)
            apply = row.find_all("td", class_="align-middle d-none d-md-table-cell")
            a = apply[1].find("a")
            href = a.get("href")
            applylink = "https://web3.career" + href
            jobstable.append([role,applylink,org,location,salary,badgeslist])

        #try:
        #    print(role,applylink,org,location,salary,badgeslist)    
        #    print("************")
        #except:
        #    print("THIS IS AN ERROR") 
        #    print("************")
    

with open("C:/Users/User/Documents/Freelance work/Media and Entertainment Innovation/Airtable/web3careers.csv", "w", encoding="utf-8") as f:
    write = csv.writer(f)
    write.writerows(jobstable)



