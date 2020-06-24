import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta
from tkinter import *
from tkinter import ttk

def offer_search():
  all_offers = []
  city = city_field.get()
  downprice = downprice_field.get()
  highprice = highprice_field.get()
  downarea = downarea_field.get()
  higharea = higharea_field.get()
  days = days_field.get()
  for element in otodom(city.lower(),downprice,highprice,downarea,higharea,days):
    all_offers.append(element)
  for element in olx(city.lower(),downprice,highprice,downarea,higharea,days):
    all_offers.append(element)
  for offer in all_offers:
    listBox.insert("","end",values=(offer[0],offer[1],offer[2],offer[3],offer[4]))

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
table.geometry("1000x340")

Label(table,text='Miasto').grid(row=0,column=0)
city_field = Entry(table)
city_field.grid(row=1,column=0)
Label(table,text='Cena minimalna [zł]').grid(row=0,column=1)
downprice_field = Entry(table)
downprice_field.grid(row=1,column=1)
Label(table,text='Cena maksymalna [zł]').grid(row=0,column=2)
highprice_field = Entry(table)
highprice_field.grid(row=1,column=2)
Label(table,text='Powierzchnia minimalna [m2]').grid(row=0,column=3)
downarea_field = Entry(table)
downarea_field.grid(row=1,column=3)
Label(table,text='Powierzchnia maksymalna [m2]').grid(row=0,column=4)
higharea_field = Entry(table)
higharea_field.grid(row=1,column=4)
Label(table,text='Dni od pojawienia się oferty').grid(row=0,column=5)
days_field = Entry(table)
days_field.grid(row=1,column=5)

Label(table, text="Znalezione oferty",font=("Arial",20)).grid(row=3, columnspan=6)
columns = ('Serwis','Tytuł','Powierzchnia','Cena','Adres URL')
listBox = ttk.Treeview(table,selectmode = 'browse',columns=columns,show='headings')
listBox.column("Serwis", minwidth=0, width=100, stretch=YES)
listBox.column("Tytuł", minwidth=0, width=300, stretch=YES)
listBox.column("Powierzchnia", minwidth=0, width=100, stretch=YES)
listBox.column("Cena", minwidth=0, width=100, stretch=YES)
listBox.column("Adres URL", minwidth=0, width=400, stretch=YES)

for column in columns:
    listBox.heading(column,text=column)
listBox.grid(row=4,column=0,columnspan=6)

submitButton = Button(table, text="Zatwierdź", command = offer_search)
submitButton.grid(row=2,column=5,pady=5)

    
table.mainloop()
