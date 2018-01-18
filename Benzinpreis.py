##################################################################
# Checking Fuel-Prices with clever-tanken.de
# author: Joerg Bilert
# Ver.: 0.5
# Date: 01-18-2018
##################################################################
import requests
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import time
from time import strftime, localtime
from bs4 import BeautifulSoup
import configparser

#contains the name and address of a station and the pulled prices of that station
class Station:
    def __init__(self, address):
        self.address = address
        self.prices = []
         
    def append(self, price):
        self.prices.append(price)
        return self.prices
    
    def print(self):
        print(self.address)
        for price in self.prices:
            print(price)

#read config.ini from the program directory
config = configparser.ConfigParser()
config.read('config.ini')

span = config['DEFAULT']['SPAN']
period = config['DEFAULT']['PERIOD']

<<<<<<< HEAD
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
=======
path = config['USER']['PATH']
html_file = config['USER']['FILE_NAME']
plz = config['USER']['PLZ']
town = config['USER']['TOWN']
radius = config['USER']['RADIUS']
fuel_type = config['USER']['FUEL_TYPE']
>>>>>>> 261bf5beb380d542d67cc0965b4815a62c657e89

#stations contains all the station_objs for a defined search
stations = []

#us parameters to generate the web-adress
source = 'http://www.clever-tanken.de/tankstelle_liste?spritsorte='+fuel_type+'&ort='+plz+'+'+town+'&r='+radius+'&sort=km'

#loads the url into the parser
def load_page(url):
    page = requests.get(url)
    content = BeautifulSoup(page.text, 'html.parser')
    return content

<<<<<<< HEAD
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
    

=======
#extract price-table from webpage
def get_stations(content):
    sta = content.find_all(class_='price-entry')
    return sta
     
#get address and creat station_obj for each station
def get_address(raw):
    for station in raw:
        #get address-info in html
        ad1 = station.find(class_='row fuel-station-location-name')
        ad2 = station.find(id = 'fuel-station-location-street')
        ad3 = station.find(id = 'fuel-station-location-city')
        
        #strip html-tags
        ad1_str = ad1.contents[0]
        ad2_str = ad2.contents[0]
        ad3_str = ad3.contents[0]
        
        #combine into address-string and create Station
        address = ad1_str +'\n'+ ad2_str +'\n'+ ad3_str
        stations.append(Station(address))
    

#extract prices from html and append do Station
def extract_price(raw):
    x = 0
    for station in raw:
        price_temp = station.find(class_="price")
        
        #check wether the station really offers a price for the selected fueltype at the selected time
        if price_temp ==None:
            price = None
        else:
            price = float(price_temp.contents[0])
        
        stations[x].append(price)
        x += 1
        
#plot the data and publish it as html
def plotter(stations, times):
    layout = dict(xaxis = dict(title = 'Zeitpunkt'),
                  yaxis = dict(title = 'Preis'),
                  )
    data = []
    for station in stations:
        #print(station.address)
        plot = go.Scatter(name = station.address, x = times, y = station.prices)
        data.append(plot)
    
    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig, filename=path+html_file, auto_open=False)
>>>>>>> 261bf5beb380d542d67cc0965b4815a62c657e89
    
#run the mainloop
counter = 0
clock = [] #save the timestamp of each scan

while counter < (48*int(span)):
    clock.append(strftime('%x - %H:%M', localtime()))
    website = load_page(source)
    fuelstations = get_stations(website)
    get_address(fuelstations)
    extract_price(fuelstations)
    plotter(stations, clock)
    counter +=1
    time.sleep(int(period))
    
