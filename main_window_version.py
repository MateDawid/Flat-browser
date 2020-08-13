import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta
from tkinter import *
import webbrowser

def openweb(website):
  webbrowser.open_new(website)

def offer_search():
  all_offers = []
  city = city_field.get()
  downprice = downprice_field.get()
  highprice = highprice_field.get()
  downarea = downarea_field.get()
  higharea = higharea_field.get()
  days = days_field.get()
  #searching all websites
  for element in otodom(city.lower(),downprice,highprice,downarea,higharea,days):
    all_offers.append(element)
  for element in olx(city.lower(),downprice,highprice,downarea,higharea,days):
    all_offers.append(element)
  #adding offers to table
  total_rows = len(all_offers)
  total_columns = len(all_offers[0])
  for i in range(total_rows): 
    for j in range(4):
        final_offer = Entry(table,width=30,font=("Arial",10))
        final_offer.grid(row=i+5,column=j+2)
        final_offer.insert(END,all_offers[i][j])
    website = all_offers[i][4]
    final_offer = Button(table,text = "Przejdź",command=lambda aurl=website:openweb(aurl))
    final_offer.grid(row=i+5,column=6)
def otodom (city,price_from,price_to,area_from,area_to,days):
   
    adress = "https://www.otodom.pl/sprzedaz/mieszkanie/"+city+"/?search%5Bcreated_since%5D="+days+"&search%5Bfilter_float_price%3Afrom%5D="+price_from+"&search%5Bfilter_float_price%3Ato%5D="+price_to+"&search%5Bfilter_float_m%3Afrom%5D="+area_from+"&search%5Bfilter_float_m%3Ato%5D="+area_to+"&nrAdsPerPage=72" 
    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("article",attrs={"class":"offer-item"})
    offers = []
    for element in elements:
        city_name = city.capitalize()
        if city_name in str(element.find('p',class_="text-nowrap").text.strip()):
            offerTitle = element.find('span',class_="offer-item-title")
            price = element.find('li',class_="offer-item-price")
            area = element.find('li',class_="hidden-xs offer-item-area")
            URL = element['data-url']
            offers.append(['otodom.pl',offerTitle.text.strip(),area.text.strip(),price.text.strip(),URL])
    return offers
def olx(city,price_from,price_to,area_from,area_to,days):
    
    months_numbers = {"stycznia":1,"lutego":2,"marca":3,"kwietnia":4,"maja":5,"czerwca":6,"lipca":7,"sierpnia":8,"września":9,"października":10,"listopada":11,"grudnia":12}
    adress = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/"+city+"/?search%5Bfilter_float_price%3Afrom%5D="+price_from+"&search%5Bfilter_float_price%3Ato%5D="+price_to+"&search%5Bfilter_float_m%3Afrom%5D="+area_from+"&search%5Bfilter_float_m%3Ato%5D="+area_to+"&view=list"

    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("tr",attrs={"class":"wrap"})
    offers = []

    for element in elements:
        URL = element.find('a',href = True)['href'] 
        if URL.startswith("https://www.olx.pl/"):
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
              offers.append(['olx.pl',offerTitle.text.strip(),area.text.strip(),price.text.strip(),URL])
            else:
              continue
          else:
            offers.append(['olx.pl',offerTitle.text.strip(),area.text.strip(),price.text.strip(),URL])
        else:
          continue
    return offers

#table creating

table = Tk()
table.geometry("1300x700")

#data entry fields
Label(table,text='Miasto').grid(row=0,column=1)
city_field = Entry(table)
city_field.grid(row=1,column=1)
Label(table,text='Cena minimalna [zł]').grid(row=0,column=2)
downprice_field = Entry(table)
downprice_field.grid(row=1,column=2)
Label(table,text='Cena maksymalna [zł]').grid(row=0,column=3)
highprice_field = Entry(table)
highprice_field.grid(row=1,column=3)
Label(table,text='Powierzchnia minimalna [m2]').grid(row=0,column=4)
downarea_field = Entry(table)
downarea_field.grid(row=1,column=4)
Label(table,text='Powierzchnia maksymalna [m2]').grid(row=0,column=5)
higharea_field = Entry(table)
higharea_field.grid(row=1,column=5)
Label(table,text='Dni od pojawienia się oferty').grid(row=0,column=6)
days_field = Entry(table)
days_field.grid(row=1,column=6)

#submitting offer searching

submitButton = Button(table, text="Zatwierdź", command = offer_search)
submitButton.grid(row=1,column=7,pady=5)

#table with flat offers

Label(table, text="Znalezione oferty",font=("Arial",20)).grid(row=3,column=2, columnspan=5)
columns = ('Serwis','Tytuł','Powierzchnia','Cena')
for i in range(len(columns)):
  header = Entry(table,width=30,font=("Arial",10,'bold'))
  header.grid(row = 4,column = i+2)
  header.insert(END,columns[i])
table.mainloop()