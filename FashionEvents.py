import requests
import urllib
from bs4 import BeautifulSoup
import csv
import json

path =  "C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/FashionEvents/"
results = [["Event Name","About Event","Location","Date From","Date to","Profile URL","Website"]]

for i in range(1,15):
    
    print("Webscraping page ",str(i))
    file = path + "page " + str(i) + ".html"
    soup = BeautifulSoup(open(file, encoding="utf8"), "html.parser")

    body = soup.body

    div = body.find("div", class_="css-1ezg1vh")
    ul = div.find("ul", class_="MuiList-root fu-mdc-list MuiList-padding")
    li = ul.find_all("li")

    for e in li:
        a = e.find("a")
        if a != None:
            script = a.find("script")
            json_object = json.loads(script.contents[0])
            EventName = json_object["name"]
            AboutEvent = json_object["description"]
            loc_dict = json_object["location"]
            address = loc_dict["address"]
            Location = address["addressLocality"] + ", " + address["addressCountry"]
            DateFrom = json_object["startDate"].split(",")
            DateFrom = DateFrom[0]
            DateTo = json_object["endDate"].split(",")
            DateTo = DateTo[0]
            profileURL = json_object["url"]
            results.append([EventName,AboutEvent,Location,DateFrom,DateTo,profileURL])
            res = requests.get(profileURL)
            soup1 = BeautifulSoup(res.content, "html.parser")
            body1 = soup1.body
            main = body1.find("main")
            try:
                urllist = main.find_all("a")
                Website = urllist[3]["href"]
                results[len(results)-1].append(Website)
            except:
                results[len(results)-1].append("Website not available")
            

with open("C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/FashionEvents.csv", "w", encoding="utf-8") as f:
    write = csv.writer(f)
    write.writerows(results)




