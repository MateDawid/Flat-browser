from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import webbrowser

from site_searching import *

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
  offers_table.title("FlatBrowser")
  label_text = "Offers found: "+str(len(all_offers))
  offers_table.geometry("950x600")

  # adding scrollbar

  main_frame = Frame(offers_table)
  main_frame.pack(fill=BOTH, expand=1)

  my_canvas = Canvas(main_frame)
  my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

  my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
  my_scrollbar.pack(side=RIGHT, fill=Y)

  my_canvas.configure(yscrollcommand=my_scrollbar.set)
  my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

  second_frame = Frame(my_canvas)

  my_canvas.create_window((0,0), window=second_frame, anchor = "nw")

  # table with flat offers
  Label(second_frame, text=label_text,font=("Arial",20)).grid(row=0,column=2, columnspan=5)
  Label(second_frame, text="").grid(row=1,column=0, columnspan=1)
  columns = ('Site','Title','Area','Price')
  for i in range(len(columns)):
    if columns[i] != "Title":
      header = Entry(second_frame,width=20,font=("Arial",10,'bold'),justify='center')
      header.grid(row = 1,column = i+2)
      header.insert(END,columns[i])
    else:
      header = Entry(second_frame,width=60,font=("Arial",10,'bold'),justify='center')
      header.grid(row = 1,column = i+2)
      header.insert(END,columns[i])  

  # adding offers to table
  total_rows = len(all_offers)
  for i in range(total_rows): 
    for j in range(4):
      if j!=1:
        final_offer = Entry(second_frame,width=20,font=("Arial",10),justify='center')
        final_offer.grid(row=i+5,column=j+2)
        final_offer.insert(END,all_offers[i][j])
      else:
        final_offer = Entry(second_frame,width=60,font=("Arial",10))
        final_offer.grid(row=i+5,column=j+2)
        final_offer.insert(END,all_offers[i][j])
    website = all_offers[i][4]
    final_offer = Button(second_frame,text = "Website",command=lambda aurl=website:open_web(aurl))
    final_offer.grid(row=i+5,column=6)

  # Information after finishing searching
  messagebox.showinfo("Info","Searching finished. We've found "+str(len(all_offers))+" offers.")
  offers_table.mainloop()


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