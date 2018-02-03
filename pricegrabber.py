import numpy as np
import requests
import time
from time import strftime, localtime
import datetime
from bs4 import BeautifulSoup

import sqlite3
import pandas as pd
import sys
from pathlib import Path



if len(sys.argv) < 3:
    print ('''Bitte Postleitzahl und Ort angeben!\n\n
python3 pricegrabber.py PLZ Ort\n\n''')
    sys.exit()
else:
    plz = str(sys.argv[1])
    l = len(sys.argv)
    town = []
    ort =''
    for p in range(2,len(sys.argv)):
        town.append(sys.argv[p])
    for t in town:
        ort += "+"+t
    print(''' Serverdienst läuft und sammelt stündlich alle Kraftstoffpreise \n
im Umkreis von 50km um '''+plz +' ' +ort+'''.\n
Zum Beenden [Strg]+[C] drücken''')

#read and parse config.ini
#config = configparser.ConfigParser()
#config.read('config.ini')

#span = config['DEFAULT']['SPAN']
#period = config['DEFAULT']['PERIOD']

#plz = config['USER']['PLZ']
#town = config['USER']['TOWN']
radius = '50.0'
fuel_type = [1, 3, 4, 5, 6, 7, 8, 12]

#cheack if database exists or create one
def create_load_database():
    if Path('data.sqlite').is_file():
        db = sqlite3.connect('data.sqlite')
        print ('Database loaded')
    else:
        print ('Building Database')
        db = sqlite3.connect('data.sqlite')
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE FUELS
                        (station text,
                        distance real,
                        date text,
                        price real,
                        fuel text)
                        """)
        cursor.close()
    return db

#load the complete content of clever-tanken.de (with config)
def load_page(url):
    page = requests.get(url)
    content = BeautifulSoup(page.text, 'html.parser')
    return content

#extract price-table from webpage
def get_stations(content):
    sta = content.find_all(class_='price-entry')
    return sta

#extract the data-pieces from html and write into database
def get_data(raw, db, type, timestamp):
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
        #print(stations)

       #get prices
        price_temp = station.find(class_="price")

        #check if the station offers a price for the selected fuel at the selected time
        if price_temp == None:
            price = None
            #print(prices)
        else:
            price = float(price_temp.contents[0])

        #get distance
        distance_temp = station.find(class_='fuel-station-location-address-distance')
        distance = float(str(distance_temp.contents[1])[5:9])

        #get fueltype
        if type == 1:
            f_type = 'Autogas (LPG)'
        elif type == 3:
            f_type = 'Diesel'
        elif type == 4:
            f_type = 'Bio-Ethanol'
        elif type == 5:
            f_type = 'Super E10'
        elif type == 6:
            f_type = 'Super Plus'
        elif type == 7:
            f_type = 'Super E5'
        elif type == 8:
            f_type = 'Erdgas (CNG)'
        else:
            f_type = 'Premium Diesel'

        entry = (address, distance, timestamp, price, f_type)
        print (entry)
        # write the data into database
        cursor = db.cursor()
        cursor.execute("INSERT INTO FUELS VALUES (?,?,?,?,?)", entry)
        db.commit()
        cursor.close()


database = create_load_database()
while True:
    dt = datetime.datetime.now()
    if dt.minute == 00:
        time = strftime('%x - %H:%M', localtime())
        for type in fuel_type:
            source = 'http://www.clever-tanken.de/tankstelle_liste?spritsorte='+str(type)+'&ort='+plz+ort+'&r='+radius+'&sort=km'
            website = load_page(source)
            fuelstations = get_stations(website)
            get_data(fuelstations, database, type, time)
