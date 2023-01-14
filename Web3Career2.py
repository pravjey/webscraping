import requests
import urllib
from bs4 import BeautifulSoup
import csv
import json
import os
from pyairtable import Table


path = "https://web3.career/?page="
lastpage = 666
jobslist = []
stop = False
page = 1
api_key = "keyGgWfIqVR1Ivcbx"

while stop == False:
    print("Webscraping page ",str(page))
    url = path + str(page)
    res = requests.get(url)

    soup = BeautifulSoup(res.content, "html.parser")

    tbody = soup.tbody
    rows = tbody.find_all("tr", class_="table_row")

    for row in rows:
        time = row.find("td", class_="align-middle job-time-ago-mobile").text.strip()
        if time != "" and time[-2:] != "mo":
            if time[-1:] == "h" or (time[-1:] == "d" and int(time[:-1]) <= 7):
                if (time[len(time)-1] == "h" or time[len(time)-1] == "d"):
                    role = row.h2.text.strip()
                    org = row.h3.text.strip()
                    salary = row.p.text.strip()
                    location = row.find("td", class_="job-location-mobile").text.strip()
                    #badges = row.find("td", class_="align-middle d-none d-md-table-cell")
                    #badgeslist = []
                    #try:
                    #    badges = badges.find_all("span", class_="my-badge my-badge-secondary")
                    #    for i in badges:
                    #        a = i.find("a")
                    #        href = a.get("href")
                    #        start = href.find("/")
                    #        end = href.find("-jobs")
                    #        badge = href[start:end]
                    #        badge = badge[1:]
                    #        badge = badge.replace("-", " ")
                    #        badgeslist.append(badge)
                    #except:
                    #    badgeslist.append("")
                    a = row.find("a")
                    href = a.get("href")
                    applylink = "https://web3.career" + href
                    jobslist.append([role,applylink,org,location,salary])
            elif (time[-1:] == "d" and int(time[:-1]) > 7):
                    stop = True

    page += 1


print("Saving to Airtable/Jobs...")            
jobstable = Table(api_key, "appSzNEYk5bqsfn54", "JOBS")    

for row in jobslist:
    role = row[0]
    apply = row[1]
    org = row[2]
    loc = row[3].strip("\n")
    salary = row[4]
    if salary != "":
        currency = salary[0]
        salary = salary.strip(currency)
        salary = salary.strip(currency)
    else:
        currency = "NA"
    #desc = ""
    #for i in range(len(row[5])):
    #    if i == len(row[5])-1:
    #        desc = desc + row[5][i]
    #    else:
    #        desc = desc + row[5][i] + ", "
    jobstable.create({
        "ROLE": role,
        "Apply": apply,
        #"Description": desc,
        "Organisation.": org,
        "Location of Job": loc,
        "Salary Range": salary,
        "Currency": currency
    })
