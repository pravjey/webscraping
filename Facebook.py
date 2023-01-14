import requests
import urllib
from bs4 import BeautifulSoup
import csv


URL =  "https://fashionunited.com/i/facebook-fashion-index/"

res = requests.get(URL)

txt = res.text
status = res.status_code

soup = BeautifulSoup(res.content, "html.parser")

table = soup.tbody

companies = table.find_all("div", class_="fu-list-link")
likes = table.find_all("div", class_="fu-list-cell")

results = [["Company","Facebook","Facebook Likes"]]

for e in range(len(companies)):
    company = companies[e].text.strip()
    facebook = companies[e].a["href"].strip()
    facebookLikes = likes[e].text.strip()
    results.append([company,facebook,facebookLikes])

with open("C:/Users/User/Documents/Oxyderkis/Clients/Fashion United/Facebook.csv", "w") as f:
    write = csv.writer(f)
    write.writerows(results)




