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
html_file = config['USER']['HTML_FILE']
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

#extract stations and prices and wrtie them into Station_Objs
def get_data(content):

