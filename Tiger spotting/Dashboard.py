import pandas as pd
import numpy as np
import random

from rich.console import Console

from bokeh.plotting import figure, show, curdoc
from bokeh.models import Select, ColumnDataSource, Label
from bokeh.io import output_notebook, curdoc, output_file
from bokeh.layouts import row, column, gridplot
import matplotlib.pyplot as plt

df = pd.read_csv(r'data/EERecords.csv')

loc_df = pd.read_csv(r'data/EEtraplocs.csv')

cam_df = pd.read_csv(r'data/EECam_act.csv')

# Merge Dataframes
df1 = df.merge(loc_df, on='Trap_ID', how='inner')

df1['Ind'] = df1['Ind'].apply(lambda x: str(x))

def tiger_dist(idt):
    """Calculate distance covered in the reserve"""
    idt = tiger_sel.value
    data = df1.query('Ind==idt')
    return str([np.sqrt((x[i] - x[i+1])**2 + (y[i] - y[i+1]**2)) for x, y in zip(df1['CenteredX'], df1['CenteredY']) ].sum())

# Dropdown
tiger_sel = Select(
    title="Select Tiger",
    value="1",
    options=[str(i) for i in df1['Ind'].unique()]
)

#id_tiger = tiger_dist(tiger_sel.value)

map_line = ColumnDataSource(df1)

# Create a new plot with a title and axis labels
p = figure(
    plot_width=700,
    plot_height=400,
    title="Area chart",
    x_axis_label='X',
    y_axis_label='Y'
)

# Distance card for the Tiger
#dist_card = figure(plot_width=200, plot_height=300, title="Distance covered")

#dist_card.rect(x=0.5, y=0.5, width=1, height=1, fill_color="white", line_color="black")

# Add label to display the card's value
#value_label = Label(x=0.5, y=0.5, text=id_tiger, text_font_size="24px", text_color="red", text_align="center", text_baseline="middle")
#dist_card.add_layout(value_label)

# Add a scatter glyph with X and Y data
p.scatter(
    source=loc_df,
    x='CenteredX',
    y='CenteredY',
    size=10,
    alpha=0.5
)

p.line(
    source=map_line,
    x='CenteredX',
    y='CenteredY',
    line_width=2,
    color='red',
    legend_label="Tiger's path"
)

# Function
def tiger_line(attr, old, new):
    """Select tiger id to get its activity area"""
    idt = tiger_sel.value
    map_line.data = df1.query('Ind==@idt')

# Change using dropdown
tiger_sel.on_change('value', tiger_line)
#tiger_sel.on_change('value', id_tiger)
tiger_chart = column(tiger_sel, p)

# Output the plot to a Jupyter Notebook
curdoc().add_root(tiger_chart)
curdoc().title = "Tiger movement in Nagarahole reserve"
