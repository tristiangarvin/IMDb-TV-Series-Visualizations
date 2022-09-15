from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl

wb=openpyxl.Workbook()
sheet=wb.active

sheet.append(["Title", "Rating"])

url ="https://www.imdb.com/chart/toptv/"
req=requests.get(url)
soup=BeautifulSoup(req.text,"html.parser")
linked=soup.find("tbody",class_="lister-list")
rows=linked.find_all("tr")

with open('show_overall.csv', 'a', encoding='utf-8') as csv:
    csv.write('Title,Rating_Overall\n')
    for i in rows:
        td=i.select_one("td.titleColumn > a").text.replace("\n"," ")
        tdd=i.find("td",class_="ratingColumn imdbRating").text.replace("\n"," ")
        csv.write(td + ',' + tdd + '\n')
