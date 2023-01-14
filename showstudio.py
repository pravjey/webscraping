import requests
import urllib
from bs4 import BeautifulSoup
import csv
import json

path =  "https://www.showstudio.com/contributors?page="

contributors = [["Name","Occupation","Bio","Link"]]

for i in range(1,144):
    
    print("Webscraping page ",str(i))
    url = path + str(i)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    body = soup.body

    div = body.find_all("div", class_="relative col col-12 sm-col-4")

    for item in div:
        a = item.find("a", class_="block bg-white")
        div2 = a.find("div", class_="px4 py5 sm-pt6 sm-pb7 md-px5 md-pb8")
        link = "https://www.showstudio.com/" + str(a["href"])
        #contributor_url = "https://www.showstudio.com/" + str(link)
        #res1 = requests.get(contributor_url)
        #soup1 = BeautifulSoup(res1.content, "html.parser")
        #body1 = soup1.body
        #print(main.text)
        try:
            occupation = div2.find("span").text
        except:
            occupation = "No occupation"
        try:
            name = div2.find("h3").text
        except:
            name = "No name"
        try:
            bio = div2.find("div").text
        except:
            bio = "No bio"
        contributors.append([name, occupation, bio,link])
    
with open("C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/ShowStudio.csv", "w", encoding="utf-8") as f:
    write = csv.writer(f)
    write.writerows(contributors)




