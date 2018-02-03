# Benzinpreisanalyse
Get fuel-prices from http://clever-tanken.de and save them for price-development analysis

*written in Python 3*

This Python script uses the website http://clever-tanken.de to get the fuel-price of the gas stations in your area of choice.
The data is saved into a sqlite-database for later analysis in an application of your liking or the dashboard.py-App.

## Requirements

Check, whether you have all the necessary python-modules installed: BeautifulSoup, datetime, dash, dash_core_components, dash_html_components, dash_renderer, Plotly, Pandas, Time, NumPy, Requests or install them with
`pip3 install bs4 plotly requests datetime time pandas numpy dash dash_core_components dash_html_components dash_renderer`

## Usage

Run the grabber on your server with `nohup python3 pricegrabber.py <Postleitzahl> <Town> >grabber.log &`.  
It will wait for the full hour and then start collecting all fuel-prices for all fuel-types in an area of 50km around the place you specified when you started the script.

Then run the dashboard using `nohup python3 dashboard.py >dashboard.log &`. It offers a web-frontend where you can watch the development of prices.
Per default the dashboard can be reached under `http://<YOUR_SERVER_IP/URL>:8050`

## ToDo
+ limiting the size of the database by dropping old data.
