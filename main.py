import requests
from bs4 import BeautifulSoup
def otodom (price_from,price_to,area_from,area_to):
   
    adress = "https://www.otodom.pl/sprzedaz/mieszkanie/jaworzno/?search%5Bfilter_float_price%3Afrom%5D="+price_from+"&search%5Bfilter_float_price%3Ato%5D="+price_to+"&search%5Bfilter_float_m%3Afrom%5D="+area_from+"&search%5Bfilter_float_m%3Ato%5D="+area_to+"&search%5Bregion_id%5D=12&search%5Bsubregion_id%5D=305&search%5Bcity_id%5D=173&nrAdsPerPage=72"
        
    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("article",attrs={"class":"offer-item"})
    print("Ofert na stronie: ",len(elements))
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

downprice = input("Podaj minimalną cenę: ")
highprice = input("Podaj maksymalną cenę: ")
downarea = input("Podaj minimalny metraż: ")
higharea = input("Podaj maksymalny metraż: ")
otodom(downprice,highprice,downarea,higharea)
