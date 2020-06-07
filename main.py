import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta

months_numbers = {"stycznia":1,"lutego":2,"marca":3,"kwietnia":4,"maja":5,"czerwca":6,"lipca":7,"sierpnia":8,"września":9,"października":10,"listopada":11,"grudnia":12}

def otodom (city,price_from,price_to,area_from,area_to,days):
   
    adress = "https://www.otodom.pl/sprzedaz/mieszkanie/"+city+"/?search%5Bcreated_since%5D="+days+"&search%5Bfilter_float_price%3Afrom%5D="+price_from+"&search%5Bfilter_float_price%3Ato%5D="+price_to+"&search%5Bfilter_float_m%3Afrom%5D="+area_from+"&search%5Bfilter_float_m%3Ato%5D="+area_to+"&nrAdsPerPage=72"
        
    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("article",attrs={"class":"offer-item"})
    print("Ofert na otodom.pl: ",len(elements))
    print("="*40)
    for element in elements:
        offerTitle = element.find('span',class_="offer-item-title")
        price = element.find('li',class_="offer-item-price")
        area = element.find('li',class_="hidden-xs offer-item-area")
        URL = element['data-url']
        print("Tytuł:",offerTitle.text.strip())
        print("Cena:",price.text.strip())
        print("Powierzchnia:",area.text.strip())
        print("URL:",URL)
        print("="*40) 
def olx(city,price_from,price_to,area_from,area_to,days):

    adress = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/"+city+"/?search%5Bfilter_float_price%3Afrom%5D="+price_from+"&search%5Bfilter_float_price%3Ato%5D="+price_to+"&search%5Bfilter_float_m%3Afrom%5D="+area_from+"&search%5Bfilter_float_m%3Ato%5D="+area_to+"&view=list"

    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("tr",attrs={"class":"wrap"})
    print("Ofert na olx.pl: ",len(elements))
    print("="*40)
    for element in elements:
        URL = element.find('a',href = True)['href'] 
        offerTitle = element.find('h3',class_="lheight22 margintop5")
        price = element.find('p',class_="price")
        #connecting with offer page
        offerPage = requests.get(URL)
        offerSoup = BeautifulSoup(offerPage.content,"html.parser")
        #finding flat area
        index = 0
        details = offerSoup.findAll("li",class_="offer-details__item")
        for i in range (len(details)):
            if details[i].find('span',class_='offer-details__name').text.strip() == "Powierzchnia":
                index = i
        area = offerSoup.findAll("strong",class_="offer-details__value")[index]
        #finding offer date
        offerDate = ((offerSoup.find("li",class_="offer-bottombar__item")).find('strong')).text.strip()[9:]
        moth_number = months_numbers[(offerDate[2:-4]).strip()]
        if days != "":
            if datetime.date(int(offerDate[-4:]),int(moth_number),int(offerDate[:2]))+relativedelta(days=int(days))>datetime.date.today():
                print("Tytuł:",offerTitle.text.strip())
                print("Cena:",price.text.strip())
                print("Powierzchnia:",area.text.strip())
                print("URL:",URL)
                print("="*40)
            else:
                continue
        else:
            print("Tytuł:",offerTitle.text.strip())
            print("Cena:",price.text.strip())
            print("Powierzchnia:",area.text.strip())
            print("URL:",URL)
            print("="*40)

city = input("Podaj miasto: ")
downprice = input("Podaj minimalną cenę: ")
highprice = input("Podaj maksymalną cenę: ")
downarea = input("Podaj minimalny metraż: ")
higharea = input("Podaj maksymalny metraż: ")
days = input("Podaj liczbę dni od dodania ogłoszenia: ")

olx(city.lower(),downprice,highprice,downarea,higharea,days)
