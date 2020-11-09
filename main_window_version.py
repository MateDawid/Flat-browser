import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta
from tkinter import *
from tkinter import messagebox
import webbrowser

def open_web(website):
  webbrowser.open_new(website)

def offer_search():
  all_offers = []
  city = city_field.get()
  downprice = downprice_field.get()
  highprice = highprice_field.get()
  downarea = downarea_field.get()
  higharea = higharea_field.get()
  days = days_field.get()
  # searching all websites
  for element in otodom(city.lower(),downprice,highprice,downarea,higharea,days):
    all_offers.append(element)
  for element in olx(city.lower(),downprice,highprice,downarea,higharea,days):
    all_offers.append(element)
  for element in morizon(city.lower(),downprice,highprice,downarea,higharea,days):
    all_offers.append(element)
  
  # create table with offers
  offers_table = Tk()
  offers_table.title("FlatBrowser - Found offers")
  offers_table.geometry("930x570")


  # table with flat offers
  Label(offers_table, text="Offers found",font=("Arial",20)).grid(row=0,column=2, columnspan=5)
  Label(offers_table, text="").grid(row=1,column=0, columnspan=1)
  columns = ('Site','Title','Area','Price')
  for i in range(len(columns)):
    header = Entry(offers_table,width=30,font=("Arial",10,'bold'))
    header.grid(row = 1,column = i+2)
    header.insert(END,columns[i])

  # adding offers to table
  total_rows = len(all_offers)
  for i in range(total_rows): 
    for j in range(4):
        final_offer = Entry(offers_table,width=30,font=("Arial",10))
        final_offer.grid(row=i+5,column=j+2)
        final_offer.insert(END,all_offers[i][j])
    website = all_offers[i][4]
    final_offer = Button(offers_table,text = "Website",command=lambda aurl=website:open_web(aurl))
    final_offer.grid(row=i+5,column=6)

  # Information after finishing searching
  messagebox.showinfo("Info","Searching finished.")
  offers_table.mainloop()

def otodom (city,price_from,price_to,area_from,area_to,days):
    # Filling URL address with variables
    adress = "https://www.otodom.pl/sprzedaz/mieszkanie/"+city+"/?search%5Bcreated_since%5D="+days+"&search%5Bfilter_float_price%3Afrom%5D="+price_from+"&search%5Bfilter_float_price%3Ato%5D="+price_to+"&search%5Bfilter_float_m%3Afrom%5D="+area_from+"&search%5Bfilter_float_m%3Ato%5D="+area_to+"&nrAdsPerPage=72" 

    # Connecting with page
    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("article",attrs={"class":"offer-item"})
    offers = []
    
    # Searching offer details
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
    
    # Creating dictionary with names of moths, which will be used to define offer date
    months_numbers = {"stycznia":1,"lutego":2,"marca":3,"kwietnia":4,"maja":5,"czerwca":6,"lipca":7,"sierpnia":8,"września":9,"października":10,"listopada":11,"grudnia":12}

    # Filling URL address with variables 
    adress = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/"+city+"/?search%5Bfilter_float_price%3Afrom%5D="+price_from+"&search%5Bfilter_float_price%3Ato%5D="+price_to+"&search%5Bfilter_float_m%3Afrom%5D="+area_from+"&search%5Bfilter_float_m%3Ato%5D="+area_to+"&view=list"

    # Connecting with page
    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("tr",attrs={"class":"wrap"})
    offers = []

    # Searching offer details
    for element in elements:
        # Eliminating offers different from olx service
        URL = element.find('a',href = True)['href'] 
        if URL.startswith("https://www.olx.pl/"):
         
          # Finding title and price of flat
          offerTitle = element.find('h3',class_="lheight22 margintop5")
          price = element.find('p',class_="price")
          
          # Searching for area on offer adress
          offerPage = requests.get(URL)
          offerSoup = BeautifulSoup(offerPage.content,"html.parser")
          index = 0
          details = offerSoup.findAll("li",class_="offer-details__item")
          for i in range (len(details)):
            if details[i].find('span',class_='offer-details__name').text.strip() == "Powierzchnia":
              index = i
          area = offerSoup.findAll("strong",class_="offer-details__value")[index]
          
          # Finding offer date
          offerDate = ((offerSoup.find("li",class_="offer-bottombar__item")).find('strong')).text.strip()[9:]
          moth_number = months_numbers[(offerDate[2:-4]).strip()]
          # Converting data into proper format
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

def morizon (city,price_from,price_to,area_from,area_to,days):
    # Filling URL address with variables 
    adress = "https://www.morizon.pl/mieszkania/"+city+"/?ps%5Bprice_from%5D="+price_from+"&ps%5Bprice_to%5D="+price_to+"&ps%5Bliving_area_from%5D="+area_from+"&ps%5Bliving_area_to%5D="+area_to
    # Setting URL based on typed "days" variable
    if days == "":
      adress += ""
    elif int(days) == 1:
      adress += "&ps%5Bdate_filter%5D=1"
    elif int(days) in range(2,8):
      adress += "&ps%5Bdate_filter%5D=7"
    elif int(days) in range(8,31):
      adress += "&ps%5Bdate_filter%5D=30"
    elif int(days) in range(31,91):
      adress += "&ps%5Bdate_filter%5D=90"
    elif int(days) in range(91,181):
      adress += "&ps%5Bdate_filter%5D=180"
      
    # Connecting with page
    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("section",attrs={"class":"single-result__content single-result__content--height"})
    offers = []

    # Searching offer details
    for element in elements:
      # Avoiding elements different from offers
      if element.find("div",attrs={"class":"description single-result__description"}) == None:
        continue
      else:
        # Setting city name
        city_name = city.capitalize()

        # Finding proper title for offer
        if element.find('h3',class_="single-result__category single-result__category--title") != None:
          offerTitle = (element.find('h3',class_="single-result__category single-result__category--title")).find("p")
        else:
          offerTitle = element.find('h2',class_="single-result__title")
        
        # Finding price of flat
        price = element.find('p',class_="single-result__price")
        
        # Finding area of flat
        details = element.find('ul',class_="param list-unstyled list-inline").findAll("li")
        for detail in details:
          if detail.text.strip()[-2:] == "m²":
            area = detail
        
        # Finding URL adress of flat
        URL = element.find('a',href = True)['href']
       
        # Adding offer to list
        offers.append(['morizon.pl',offerTitle.text.strip(),area.text.strip(),price.text.replace(u'\xa0'," "),URL])
    return offers

#table creating
table = Tk()
table.title("FlatBrowser - Paramethers")
table.geometry("310x170")

#data entry fields
Label(table,text='City', width=20).grid(row=0,column=0)
city_field = Entry(table)
city_field.grid(row=0,column=1, columnspan=20)
Label(table,text='Min price [zł]').grid(row=1,column=0)
downprice_field = Entry(table)
downprice_field.grid(row=1,column=1)
Label(table,text='Max price [zł]').grid(row=2,column=0)
highprice_field = Entry(table)
highprice_field.grid(row=2,column=1)
Label(table,text='Min area [m2]').grid(row=3,column=0)
downarea_field = Entry(table)
downarea_field.grid(row=3,column=1)
Label(table,text='Max area [m2]').grid(row=4,column=0)
higharea_field = Entry(table)
higharea_field.grid(row=4,column=1)
Label(table,text='Days offer lasts').grid(row=5,column=0)
days_field = Entry(table)
days_field.grid(row=5,column=1)

# submitting offer searching
submitButton = Button(table, text="Submit", command = offer_search)
submitButton.grid(row=6,column=1,pady=5)

table.mainloop()