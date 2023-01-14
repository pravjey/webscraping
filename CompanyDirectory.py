import requests
import urllib
from bs4 import BeautifulSoup
import csv
import re

url =  "https://fashionunited.com/companies/"
results = [["Company","Country","Bio","Email","Website"]]

file =  "C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/FashionCompanyDirectory.html"

soup = BeautifulSoup(open(file, encoding="utf8"), "html.parser")
body = soup.body

ul = body.find_all("ul", class_="MuiList-root fu-mdc-list MuiList-padding")

for i in ul:
    li = i.find_all("li", class_="css-cjoe4o")
    for j in li:
        a = j.find_all("a", class_="css-1wu1n0e")
        for k in a:
            profileurl = k["href"].split('/')
            res1 = requests.get(url + profileurl[len(profileurl)-1])
            soup1 = BeautifulSoup(res1.content, "html.parser")
            body1 = soup1.body
            main = body1.find("main", class_="css-1b0accb")
            div1 = main.find("div", class_="css-oynvks")
            Company = div1.find("h1").text.strip()
            print("Webscraping details for: ", Company)
            try:
                CountryWebsite = div1.find("div", class_="css-vu3zsg").text.strip()
                CountryWebsite = CountryWebsite.split("\n")
                Website = CountryWebsite[0]
                Country = CountryWebsite[1]
            except:
                Country = "Not available"
                Website = "Website not available"
            div2 = main.find("div", class_="css-1lup18i")
            BioEmail = div2.find_all("div", class_="css-mechcd")
            try:
                Bio = BioEmail[0].text.strip()
                Email = BioEmail[1].text.strip()
                Emailsearch = re.search("E:(.*?)\n",Email)
                Email = Emailsearch.group(1)
            except:
                Email = "No Email available"


            results.append([Company, Country, Bio, Email, Website])

with open("C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/CompanyDirectory.csv", "w", encoding="utf-8") as f:
    write = csv.writer(f)
    write.writerows(results)




