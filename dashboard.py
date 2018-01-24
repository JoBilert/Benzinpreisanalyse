import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly as plot
import numpy as np


app = dash.Dash()

def data_get():
    data = []
    try:
        df = pd.read_json('test.json')
    except:
        print('No JSON-File found. \nPlease run pricegetter.py in background first!')
    for column in df.columns:
        data_temp = go.Scatter(x= df.index, y= df.ix[:,column], type='line', name= column)
        data.append(data_temp)
    return data
    
def dashboard():
    return html.Div([
        dcc.Graph(
            id='fuel-price',
            figure={'data': data_get(), 'layout': {'title':'test'}}
            )
        ])

app.layout = dashboard()

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0') #if you want to run it on a machine for development y<ou can delete the "host"


