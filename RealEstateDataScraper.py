import requests
import pandas
from bs4 import BeautifulSoup
headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
r = requests.get("https://www.buyrentkenya.com/flats-apartments-for-rent/dagoretti-north/kilimani?page=1",headers=headers)
soup = BeautifulSoup(r.content, "html.parser")
page_num=soup.find_all("a", {"class":"page-link"})[-2].text
base_url="https://www.buyrentkenya.com/flats-apartments-for-rent/dagoretti-north/kilimani?page="
l = []
for page in range(1,int(page_num)):
    new_url = base_url + str(page)
    r2 = requests.get(new_url, headers=headers)
    soup2=BeautifulSoup(r2.content,"html.parser")
    content1 = soup2.find_all("div",{"class":"result-card-item"})
    for item in content1:
        d = {}
        try:
            d["Rent Price"]=((item.find("a", {"class":"item-price"}).text).replace("KES","").replace("per month","").replace(" ",""))
        except:
            d["Rent Price"]=None
        try:
            d["Number of Beds"]=((item.find("span", {"class": "h-beds"}).text).replace(" ",""))
        except:
            d["Number of Beds"] = None
        try:
            d["Number of Baths"]=((item.find("span",{"class":"h-baths"}).text).replace(" ",""))
        except:
            d["Number of Baths"] = None
        try:
            d["Price per sq mt"]=((item.find("a",{"class":"item-sub-price"}).text).replace("KES","").replace("/m2","").replace(" ",""))
        except:
            d["Price per sq mt"]= None
        try:
            d["Property Location"]=(item.find("div",{"class": "property-location"}).text)
        except:
            d["Property Location"]=None
        l.append(d)


df = pandas.DataFrame(l)
df.to_csv("KilimaniBuyRent.csv")
