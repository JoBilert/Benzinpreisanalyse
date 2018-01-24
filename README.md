# Benzinpreisanalyse
Get fuel-prices from http://clever-tanken.de and save them for price-development analysis

*written in Python 3*

This Python script uses the website http://clever-tanken.de to get the fuel-price of the **three closest stations** in your area of choice.
The data is saved into a csv-File for later analysis in an application of your liking.

## Requirements


Check, whether you have all the necessary python-modules installed: BeautifulSoup, , dash, dash_core_components, dash_html_components, dash_renderer, Plotly, Pandas, Time, NumPy, Requests and configparser or install them with
`pip3 install bs4 plotly requests configparser time pandas numpy dash dash_core_components dash_html_components dash_renderer`

## Usage
Copy the `config.default` to `config.ini`. Edit the `config.ini` and set the Parameters:  

|Variable |Meaning|
|---------|-------|
|SPAN     |*how many shall the program run (default = 7)*|
|PERIOD   |*frequency of the scans (default = 1800 sec = 30 min)*|
|PLZ      |*enter your ZIP-Code*|
|TOWN     |*Enter the name of your town*|
|RADIUS   |*radius of the area scanned (default = 5.0km)*|
|FUEL_TYPE |*What kind of fuel are you looking for (1=Autogas (LPG), 2=LKW-Diesel, 3=Diesel, 4=Bio-Ethanol, 5=Super E10, 6=Super Plus, 7=Super E5, 8=Erdgas (CNG), 12=Premium-Diesel, 13=AdBlue)*|

Run the grabber on your server with `nohup python3 pricegrabber.py >grabber.log &`. Then run the dashboard on the using `nohup python3 dashboard.py >dashboard.log &`.

**Be advised: While the grabber stops after the amount of days you specified in SPAN in your `config.ini`, the dashboard will continue running until you terminate it manually.**

Per default the dashboard can be reached under `http://<YOUR_SERVER_IP/URL>:8050`

## ToDo
+ adding a (Web-)GUI
