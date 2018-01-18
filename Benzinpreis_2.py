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
    for station in sta:
        station_address = get_address(station)
        stations.append(Station(station_address)) 

#extrace address from price-table
def get_address(raw):
    #get address-info in html
    ad1 = raw.find(class_='row fuel-station-location-name')
    ad2 = raw.find(id = 'fuel-station-location-street')
    ad3 = raw.find(id = 'fuel-station-location-city')
    
    #strip html-tags
    ad1_str = ad1.contents[0]
    ad2_str = ad2.contents[0]
    ad3_str = ad3.contents[0]
    #combine into address-string
    address = ad1_str +'\n'+ ad2_str +'\n'+ ad3_str
    return address

#adds prices to the station_object
def get_price(content):
    sta = content.find_all(class_='price-entry')
    for station in stations:
        station.append(extract_price(sta))
        
#extract prices from html
def extract_price(raw):
    price_temp = raw.find(class_='price')
    print (price_temp)
    price = float(price_temp.contents[0])
    #print (price)
    return price
    

test = load_page(source)
test2= get_stations(test)
get_price(test)
print(stations[1].address)
print(stations[1].prices)