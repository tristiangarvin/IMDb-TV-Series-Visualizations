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
for i in rows:
    td=i.select_one("td.titleColumn > a").text.replace("\n"," ")
    tdd=i.find("td",class_="ratingColumn imdbRating").text.replace("\n"," ")
    print(td)
    print(tdd)
    sheet.append([td,tdd])
wb.save("series_overall_ratings.xlsx")  
print(wb.sheetnames)

