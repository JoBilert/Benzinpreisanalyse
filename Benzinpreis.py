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
import matplotlib.pyplot as plt, mpld3
import matplotlib.animation as animation
from matplotlib import style
from time import strftime, localtime
from bs4 import BeautifulSoup

#Set parameters and get fuel-prices from http://clever-tanken.de
path = 'e:\\'        # path where the save-file is created
filename = 'test.csv'   # name of the save-file
day = 'Sun'         # Weekday to start the scan (Use int. abbreviations: Sun, Mon, Tue, ...)
span = 7            # for how many days should the prices be checked
period = 60       # how often do you want to check the price in seconds (3600 = 1hr)

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

# start matplotlib with 4 subplots
style.use('fivethirtyeight')

fig = plt.figure()


station_1 = fig.add_subplot(3,1,1)
station_1.set_xlabel('Datum')
station_1.set_ylabel('Preis')

station_2 = fig.add_subplot(3,1,2)
station_2.set_xlabel('Datum')
station_2.set_ylabel('Preis')

station_3 = fig.add_subplot(3,1,3)
station_3.set_xlabel('Datum')
station_3.set_ylabel('Preis')

#station_4 = fig.add_subplot(2,2,4)
#station_4.set_xlabel('Datum')
#station_4.set_ylabel('Preis')

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

def animate(i):
    price_s1.append(p[0])
    price_s2.append(p[1])
    price_s3.append(p[2])
    #price_s4.append(p[3])
    
    dates.append(strftime('%x - %H:%M', localtime()))
    station_1.clear()
    station_1.plot(dates, price_s1)
    station_2.clear()
    station_2.plot(dates, price_s2)
    station_3.clear()
    station_3.plot(dates, price_s3)
#wait until the weekday arrives when you want to start the scan
#while strftime('%a') != day:
#    time.sleep(period)

#create a csv-file
output = open(path+filename, 'w', newline = '')
dates = []
price_s1 = []
price_s2 = []
price_s3 = []
price_s4 = []

#write data into output
with output:
    a, b, c, d = get_data(load_page(source))
    p, ad = stripped(a, b, c, d) #get price and address
    header = ['Datum u. Zeit', ad[0], ad[1], ad[2]]
    
    station_1.set_title(ad[0])
    station_2.set_title(ad[1])
    station_3.set_title(ad[2])
    ani = animation.FuncAnimation(fig, animate, 3600100)
    #plt.show()
    mpld3.show()
    #print(header)
    result = csv.writer(output)
    result.writerow(header)

    x = 0
    
    while x < (24*span):
        clock = strftime('%x - %H:%M', localtime()) 
        a, b, c, d = get_data(load_page(source))
        p, ad = stripped(a, b, c, d) #get price and address
        
        price_s1.append(p[0])
        price_s2.append(p[1])
        price_s3.append(p[2])
        
        entry = [clock, p[0].replace('.',','), p[1].replace('.',','), p[2].replace('.',',')] #, p[3].replace('.',',')]
        #print(entry)
        # output = open('benzinpreise.csv', 'w', newline = '') - need to check if that is necessary
        result.writerow(entry)
        x += 1
        time.sleep(period)
    
    output.close()
    

