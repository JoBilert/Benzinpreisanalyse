###########################################
# Fuel-price-scanner
###########################################

import numpy as np
import requests
import time
from time import strftime, localtime

from bs4 import BeautifulSoup

import configparser
import pandas as pd

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
            
#read the config.ini
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
source = 'http://www.clever-tanken.de/tankstelle_liste?spritsorte='+fuel_type+'&ort='+plz+'+'+town+'&r='+radius+'&sort=km' 

#initialize stations and dates
df = pd.DataFrame()
stations= []
prices=[]
clock=[]
#load the complete content of clever-tanken.de (with config)
def load_page(url):
    page = requests.get(url)
    content = BeautifulSoup(page.text, 'html.parser')
    return content

#extract price-table from webpage
def get_stations(content):
    sta = content.find_all(class_='price-entry')
    return sta

#get address and creat station_obj for each station
def get_data(raw, df):
    #prices = []
    #stations  = []
    
    x = 0
    timestamp = strftime('%x - %H:%M', localtime())
    clock.append(timestamp)
    #get adresses
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
        stations.append(address)
        #print(stations)
       
       #get prices
        price_temp = station.find(class_="price")
        
        #check if the station offers a price for the selected fuel at the selected time
        if price_temp == None:
            price = None
            prices.append(price)
            #print(prices)
        else:
            price = float(price_temp.contents[0])
            
            prices.append(price)
            #print(prices)
            
    dictionary = dict(zip(stations, prices))    
    df = pd.DataFrame(dictionary, index=clock)    
        
    return df

def write_json (df):
    df.to_json('test.json')
    

counter = 0
while counter < (((3600*24)/int(period))*int(span)):
    website = load_page(source)
    fuelstations = get_stations(website)
    data = get_data(fuelstations, df)
    print(data)
    write_json(data)
    #plotter(stations, clock)
    counter +=1
    time.sleep(int(period))


