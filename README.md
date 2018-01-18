# Benzinpreisanalyse
Get fuel-prices from http://clever-tanken.de and save them for price-development analysis

*written in Python 3*

This Python script uses the website http://clever-tanken.de to get the fuel-price of the **three closest stations** in your area of choice.
The data is saved into a csv-File for later analysis in an application of your liking.

## Requirements
Check, whether you have all the necessary python-modules installed: BeautifulSoup, Plotly, Requests and configparser or install them with
`pip3 install bs4 plotly requests configparser`

## Usage
Copy the `config.default` to `config.ini`. Edit the `config.ini` and set the Parameters:  

|Variable |Meaning|
|---------|-------|
|PATH     |*the path where you want to save your results*|
|FILE_NAME |*the name of the csv-file*                    |
|SPAN     |*how many shall the program run (default = 7)*|
|PERIOD   |*frequency of the scans (default = 1800 sec = 30 min)*|
|PLZ      |*enter your ZIP-Code*|
|TOWN     |*Enter the name of your town*|
|RADIUS   |*radius of the area scanned (default = 5.0km)*|
|FUEL_TYPE |*What kind of fuel are you looking for (1=Autogas (LPG), 2=LKW-Diesel, 3=Diesel, 4=Bio-Ethanol, 5=Super E10, 6=Super Plus, 7=Super E5, 8=Erdgas (CNG), 12=Premium-Diesel, 13=AdBlue)*|

Run the program on your server with `python3 Benzinpreis.py`. After the program finished running you can copy the csv file and open it in any application you think appropriate for analysis.

The data is output as graph in the file `index.html` in `path`. The file gets updated with every iteration.


## ToDo
+ adding a (Web-)GUI
+ get the number of stations in your area and print each of them
+ error-handling 


