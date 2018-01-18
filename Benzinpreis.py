##################################################################
# Checking Fuel-Prices with clever-tanken.de
# author: Joerg Bilert
# Ver.: 0.0
# Date: 01-12-2018
##################################################################

'''The script checks the fuel price in an area of your choice.
   You can set the fuel-type and how often the prices are checked each
   day. You can also set for how many days the prices are logged.
   The results will be saved in a csv-File (delimiter is a ";") and
   can be used in LibreOfficeCalc e.g. to find rules when prices are
   usually low.'''

import requests
import time
import csv
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
from time import strftime, localtime
from bs4 import BeautifulSoup

#generates station-obj containing the add and the prices
class Station:
    def __init__(self, address):
        self.address = address
        self.prices = []
    
    
        
    def append(self, price):
        self.prices.append(price)
        return self.prices

    
    
#Set parameters and get fuel-prices from http://clever-tanken.de
path = '' # path where the save-file is created
day = 'Sun'         # Weekday to start the scan (Use int. abbreviations: Sun, Mon, Tue, ...)
span = 7            # for how many days should the prices be checked
period = 1800       # how often do you want to check the price in seconds (3600 = 1hr)

#parameters for the web-request
PLZ = '91586'       # the ZIP-Code of the town
town = 'Lichtenau'  # the actual name of the town
radius = '5.0'      # the radius in which to check prices here 5km
fueltype = '5'      # the fuel-type you are looking for 1=Autogas (LPG)
                    #                                   2=LKW-Diesel
                    #                                   3=Diesel
                    #                                   4=Bio-Ethanol
                    #                                   5=Super E10
                    #                                   6=Super Plus
                    #                                   7=Super E5
                    #                                   8=Erdgas (CNG)
                    #                                   12=Premium-Diesel
                    #                                   13=AdBlue

#adding the parameters to search the database of clever-tanken.de
source = 'http://www.clever-tanken.de/tankstelle_liste?spritsorte='+fueltype+'&ort='+PLZ+'+'+town+'&r='+radius+'&sort=km'

#loads the url into the parser
def load_page(url):
    page = requests.get(url)
    content = BeautifulSoup(page.text, 'html.parser')
    return content

#extract prices, station,address and time
def get_data(content):
    price_tag = content.find_all(class_='price')
    station_tag = content.find_all(class_='row fuel-station-location-name')
    street_tag = content.find_all(id = 'fuel-station-location-street')
    location_tag = content.find_all(id = 'fuel-station-location-city')
    return price_tag, station_tag, street_tag, location_tag

#strip tags and get text only
def stripped (p_tag, sta_tag, str_tag, loc_tag):
    #set the lists
    price =[]
    station = []
    street = []
    loc = []
    address = []
    
    if len(p_tag) != sta_tag:
    
    #extract texts
    for p in p_tag:
        p_temp = p.contents[0]
        price.append(p_temp)
    for sta in sta_tag:
        sta_temp = sta.contents[0]
        station.append(sta_temp)
    for str in str_tag:
        str_temp = str.contents[0]
        street.append(str_temp)
    for l in loc_tag:
        l_temp = l.contents[0]
        loc.append(l_temp)
    
    # add station, street & loc into address
    for a in range(len(price)):
        address.append(station[a] + '\n' + street[a] + '\n' + loc[a])
    
    return price, address

#plot with plotly
def plotter(p1, p2, p3, c, ad):
    layout = dict(xaxis = dict(title = 'Zeitpunkt'),
                  yaxis = dict(title = 'Preis'),
                  )
   
    plot1 = go.Scatter(name=ad[0],x=c, y=p1)
    plot2 = go.Scatter(name=ad[1],x=c, y=p2)
    plot3 = go.Scatter(name=ad[2],x=c, y=p3)
    
    data = [plot1, plot2, plot3]
    
    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig, filename=path+'index.html', auto_open=False)
   

#wait until the weekday arrives when you want to start the scan
#while strftime('%a') != day:
#    time.sleep(period)'''

#create a csv-file
output = open(path+filename, 'w', newline = '')
dates = []
price_s1 = []
price_s2 = []
price_s3 = []
price_s4 = []


a, b, c, d = get_data(load_page(source))
prices, ad = stripped(a, b, c, d) #get price and address
stations = []

for i in len(prices):
    station_temp = station(ad[i])

stations.append(station_temp)
        
x = 0
    
while x < (48*span):
    #get timestamp
    clock = strftime('%x - %H:%M', localtime())
    dates.append(clock)
    
    #get data
    a, b, c, d = get_data(load_page(source))
    prices, ad = stripped(a, b, c, d) #get price and address
    
    for p in range(len(ad)):
        if 
    
        
    price_s1.append(p[0])
    price_s2.append(p[1])
    price_s3.append(p[2])
        
        plotter(price_s1, price_s2, price_s3, dates, ad)
        x += 1
        time.sleep(period)
    

    

