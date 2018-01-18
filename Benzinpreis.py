##################################################################
# Checking Fuel-Prices with clever-tanken.de
# author: Joerg Bilert
# Ver.: 0.5
# Date: 01-12-2018
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

path = config['USER']['PATH']
html_file = config['USER']['FILE_NAME']
plz = config['USER']['PLZ']
town = config['USER']['TOWN']
radius = config['USER']['RADIUS']
fuel_type = config['USER']['FUEL_TYPE']

#stations contains all the station_objs for a defined search
stations = []

#us parameters to generate the web-adress
source = 'http://www.clever-tanken.de/tankstelle_liste?spritsorte='+fuel_type+'&ort='+plz+'+'+town+'&r='+radius+'&sort=km'

#loads the url into the parser
def load_page(url):
    page = requests.get(url)
    content = BeautifulSoup(page.text, 'html.parser')
    return content

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
        if price_temp ==None:
            price = None
        else:
            print (price_temp)
            price = float(price_temp.contents[0])
        #print (price)
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
    plotly.offline.plot(fig, filename=html_file, auto_open=False)
    
#run the mainloop
counter = 0
clock = [] #save the timestamp of each scan

while counter < (((3600*24)/int(period))*int(span)):
    clock.append(strftime('%x - %H:%M', localtime()))
    website = load_page(source)
    fuelstations = get_stations(website)
    get_address(fuelstations)
    extract_price(fuelstations)
    plotter(stations, clock)
    counter +=1
    time.sleep(int(period))
    
