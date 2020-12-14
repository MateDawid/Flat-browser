import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta

def otodom (city,price_from,price_to,area_from,area_to,days):
    # Filling URL address with variables
    adress_city = city.replace(" ","-").replace("ą","a").replace("ę","e").replace("ć","c").replace("ń","n").replace("ó","o").replace("ś","s").replace("ó","o").replace("ź","z").replace("ż","z")
    adress = "https://www.otodom.pl/sprzedaz/mieszkanie/"+adress_city+"/?search%5Bcreated_since%5D="+days+"&search%5Bfilter_float_price%3Afrom%5D="+price_from+"&search%5Bfilter_float_price%3Ato%5D="+price_to+"&search%5Bfilter_float_m%3Afrom%5D="+area_from+"&search%5Bfilter_float_m%3Ato%5D="+area_to+"&nrAdsPerPage=72" 

    # Connecting with page
    page = requests.get(adress)
    soup = BeautifulSoup(page.content,"html.parser")
    elements = soup.findAll("article",attrs={"class":"offer-item"})
    offers = []
    
    # Searching offer details
    for element in elements:
        city_name = city.title()
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
    adress_city = city.replace(" ","-").replace("ą","a").replace("ę","e").replace("ć","c").replace("ń","n").replace("ó","o").replace("ś","s").replace("ó","o").replace("ź","z").replace("ż","z")
    adress = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/"+adress_city+"/?search%5Bfilter_float_price%3Afrom%5D="+price_from+"&search%5Bfilter_float_price%3Ato%5D="+price_to+"&search%5Bfilter_float_m%3Afrom%5D="+area_from+"&search%5Bfilter_float_m%3Ato%5D="+area_to+"&view=list"

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
    if days != "":  
        if int(days) == 1:
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
        try:
          offers.append(['morizon.pl',offerTitle.text.strip(),area.text.strip(),price.text.replace(u'\xa0'," "),URL])
        except:
          continue
    return offers