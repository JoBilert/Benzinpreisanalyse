import sqlite3
import pandas as pd
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


#fueltype = "Super E10"
app = dash.Dash()

app.layout = html.Div([
    html.H1(children = 'Benzinpreisbarometer'),
    html.Div([
        html.Div([
            html.P('Suchradius:', style ={'color':'black'}),
            dcc.Slider(id='distance',
                       min=5.0,
                       max=50.0,
                       step=5.0,
                       marks={i: '{}km'.format(i) for i in [5,10,15,20,25,30,35,40,45,50]},
                       value=5.0),
                 ], style={'margin-left': 50, 'margin-right':50, 'margin-bottom':30}),
        html.Div([
            html.P('Kraftstoffart:', style ={'margin-top':'10','color':'black'}),
            dcc.Dropdown(id='fueltype_choice',
                         options=[
                             {'label': 'Autogas (LPG)', 'value': 'Autogas (LPG)'},
                             {'label': 'Diesel', 'value': 'Diesel'},
                             {'label': 'Bio-Ethanol', 'value': 'Bio-Ethanol'},
                             {'label': 'Super E10', 'value': 'Super E10'},
                             {'label': 'Super Plus', 'value': 'Super Plus'},
                             {'label': 'Super E5', 'value': 'Super E5'},
                             {'label': 'Erdgas (CNG)', 'value': 'Erdgas (CNG)'},
                             {'label': 'Premium Diesel', 'value': 'Premium Diesel'}
                             ],
                         value='Super E10')
            ], style={'margin-left': 50, 'margin-right':50, 'margin-bottom':20}),
        html.Div([
            html.Div([
                html.H4('Aktuelle Preiskurve'),
                dcc.Graph(id='fuel'),
                
                ], style = {'width' : '95%', 'margin':'auto'}),
            html.Div([
                html.H4('Durchschnittspreis für diese Kraftstoffart:'),
                dcc.Graph(id='average')
                ], style = {'width' : '95%', 'margin':'auto'})
            ], style = {'margin':'auto', 'width': '95%'}),
        #html.Div([
            
         #   ], style={'margin-left': 50, 'margin-right': 50, 'margin-top': 10})
        ])
    ], style={'background-color': '#A9E2F3'})

def load_database():
    if Path('data.sqlite').is_file():
        db = sqlite3.connect('data.sqlite')
        print ('Database loaded')
        return db
    else:
        print ('!!!ERROR!!! - No database found! \n Please start the pricegrabber first.')
        return

def prepare_database(data, fuel_type, dist):
    check  = 'select * from FUELS WHERE fuel = "'+str(fuel_type)+'" AND distance <='+ str(dist)+';'
    df = pd.read_sql_query(check, data)
    return df

#plot the actual orive.curve
@app.callback(Output('fuel', 'figure'),
              [Input('fueltype_choice', 'value'),
               Input('distance', 'value')
               ]
              )
def prepare_plot(fueltype_choice, dist):
       
    figures = []
    data = load_database()
    frame = prepare_database(data, fueltype_choice, dist)
            
    for i in frame.station.unique():
        dat = go.Scatter(x = frame[frame['station'] == i]['date'],
                          y = frame[frame['station'] == i]['price'],
                          mode = 'line',
                          name = i
                          )
        figures.append(dat)
        
    return {
        'data': figures,
        'layout': go.Layout(xaxis={'title': 'Zeitpunkt'},
                            yaxis={'title': 'Preis'},
                            )
        }

#average fuel-price
@app.callback(Output('average', 'figure'),
              [Input('fueltype_choice', 'value')
               ]
              )
def plot_average(fueltype_choice):
    #load database
    data = load_database()
    #prepare dataframe
    frame = prepare_database(data, fueltype_choice, 50.0)
    frame_avg = frame.copy()
    frame_avg = frame_avg.drop(['distance', 'fuel', 'station'], axis = 1)
    #caluclate average price
    ref = str(frame_avg.loc[[0],['date']])
    print (ref)
    prices = []
    prices_avg = []
    dates = []
    for index, row in frame_avg.iterrows():
        test = str(row['date'])
        #print (test in ref)
        if test in ref:
            print (row['price'])
            if pd.isnull(row['price']) == False:
                prices.append(float(row['price']))
                avg = sum(prices) / len(prices)
            #print(avg)
            date = test
        else:
            #print('neue Zeit')
            prices_avg.append(round(avg,2))
            dates.append(date)
            ref = str(row['date'])
            date = test
            #print(ref)
            prices = []
            if pd.isnull(row['price']) == False:
                prices.append(float(row['price']))
           
    dates.append(date)
    dat = go.Scatter(x = dates,
                     y = prices_avg,
                     mode = 'line',
                     )
    print (dat)
    return {
        'data': [dat],
        'layout': go.Layout(xaxis={'title': 'Zeitpunkt'},
                            yaxis={'title': 'Preis'},
                            legend={'x': 1, 'y':-2}
                            )
        }
    

if __name__ == '__main__':
    app.run_server()
