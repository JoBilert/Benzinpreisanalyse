import requests
from bs4 import BeautifulSoup

source = 'http://www.clever-tanken.de/tankstelle_liste?spritsorte=5&ort=91586+Lichtenau&r=5&sort=km&page=10'
page = requests.get(source)
content = BeautifulSoup(page.text, 'html.parser')
sta = content.find_all(class_='price-entry')
print (sta)