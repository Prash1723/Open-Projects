import pandas as pd
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.animation as ani
import seaborn as sns
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
from plotly.subplots import make_subplots

import warnings
warnings.filterwarnings('ignore')

# Load Dataset
df = pd.read_csv(r'data/supermarket_sales - Sheet1.csv')

df['month'] = df.Date.apply(lambda x: x.split('/')[0])

#df.Date = pd.to_datetime(df.Date)

df['GMV'] = df.Total.cumsum()

df.sort_values(by='Date', ascending=True)

item_series = df.groupby(['Date', 'month']).apply(lambda s: pd.Series({
    'GMV': s['Total'].sum(),
    'total_qty': s['Quantity'].sum(),
    'total_income': s['gross income'].sum()
})).reset_index()

item_series['%Growth'] = item_series['GMV'].pct_change()

product_series = df.groupby(['Date', 'month', 'Product line']).apply(lambda s: pd.Series({
    'GMV': s['Total'].sum(),
    'total_qty': s['Quantity'].sum(),
    'total_income': s['gross income'].sum()
})).reset_index()

product_series['%Growth'] = product_series['GMV'].pct_change()

pi_series = pd.concat([item_series, product_series])

pi_series.fillna('Total', axis=1, inplace=True)

pi_series['month'] = pi_series.Date.apply(lambda x: x.split('/')[0])

pi_series.Date = pd.to_datetime(pi_series.Date)

pi_series = pi_series.sort_values(by=['Date', 'Product line'], ascending=True)

product_cat = ["Total", "Electronic accessories", "Fashion accessories", "Food and beverages",
               "Health and beauty", "Home and lifestyle", "Sports and travel"]

df.Date = pd.to_datetime(df.Date)

# Dash app
app = Dash(__name__)

pdn = dcc.Dropdown(id="product-line", 
                   options=[
                       {"label": y, "value": y}
                       for y in product_cat
                   ],
                   value="Total",
                   maxHeight=100)

mdn = dcc.Dropdown(id="month-num", 
                   options=[
                       {"label": y, "value": y}
                       for y in ["1", "2", "3"]
                       ],
                   value="1",
                   maxHeight=100)

cdn = dcc.Dropdown(id="customer-type", 
                   options=[
                       {"label": y, "value": y}
                       for y in df['Customer type'].unique()
                   ],
                   value="Member",
                   maxHeight=100)

chart1 = dcc.Graph(id="time1")
chart2 = dcc.Graph(id="time2")
chart3 = dcc.Graph(id="hist")
chart4 = dcc.Graph(id="time4")

app.layout = html.Div([
    html.H1("Sales Analysis Dashboard"),
    html.Div([
        html.Label("Type of Product"), 
        pdn,
        html.Label("Month of the year"), 
        mdn,
        html.Label("Method of payment"),
        cdn
        ],
        style={'columnCount': 3}
        ),
    html.Div([
        html.Label("Growth in Sales per day"),
        chart1,
        html.Label("Ratings per day"),
        chart3,
        html.Label("Quantity sold per day"),
        chart2,
        html.Label("Quantity sold under each product line"),
        chart4
        ],
        style={'columnCount': 2}
        )
    ])

@app.callback(
    Output("time1", 'figure'),
    Output("time2", 'figure'),
    Output("hist", 'figure'),
    Output("time4", 'figure'),
    Input("product-line", 'value'),
    Input("month-num", 'value'),
    Input("customer-type", 'value')
)

def update_graph(line, month_num, cust):
    fil_data = pi_series
    hist_data = df
    
    if line:
        fil_data = pi_series.query('`Product line`==@line')
        hist_data = df.query('`Product line`==@line')

    if cust:
        hist_data = df.query('`Customer type`==@cust')

    if month_num:
        fil_data = pi_series.query('month==@month_num')
        hist_data = df.query('month==@month_num')

    prod_gb = round(df.query('`Customer type`==@cust and month==@month_num').groupby(['Date', 'City'])['Quantity'].mean()).reset_index()

    prod_gb.columns = ['Date', 'City', 'token']

    fil_data1 = round(df.query('month==@month_num').groupby('Date').apply(lambda s: pd.Series({
    'GMV': s['Total'].sum(),
    'total_qty': s['Quantity'].sum()
    }))).reset_index()

    fil_data1['Growth%'] = round(fil_data1['GMV'].pct_change()*100, 2)

    fig1 = px.line(fil_data1, x='Date', y='Growth%')
    fig2 = px.bar(fil_data, x='Date', y='total_qty', color='Product line')
    fig1.update_yaxes(title_text="Growth %", secondary_y=False)
    fig2.update_yaxes(title_text="Quantity sold", secondary_y=False)
    fig3 = px.histogram(hist_data, x='Rating', color='City')
    fig4 = px.area(prod_gb, x='Date', y='token', color='City')
    fig4.update_yaxes(title_text="Quantity sold", secondary_y=False)
    
    return fig1, fig2, fig3, fig4

if __name__ == '__main__':
    app.run()
