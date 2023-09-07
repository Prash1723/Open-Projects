import pandas as pd
import numpy as np
import random

from rich.console import Console

from bokeh.plotting import figure, show, curdoc
from bokeh.models import Select, ColumnDataSource
from bokeh.io import output_notebook, curdoc, output_file
from bokeh.layouts import row, column, gridplot
import matplotlib.pyplot as plt

df = pd.read_csv(r'data/EERecords.csv')

loc_df = pd.read_csv(r'data/EEtraplocs.csv')

cam_df = pd.read_csv(r'data/EECam_act.csv')

# Merge Dataframes
df1 = df.merge(loc_df, on='Trap_ID', how='inner')

df1['Ind'] = df1['Ind'].apply(lambda x: str(x))

tiger_sel = Select(
    title="Select Tiger",
    value="1",
    options=[str(i) for i in df1['Ind'].unique()]
)

map_line = ColumnDataSource(df1)

# Create a new plot with a title and axis labels
p = figure(
    title="Area chart",
    x_axis_label='X',
    y_axis_label='Y'
)

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
    legend_label='Ind'
)

# Function
def tiger_line(attr, old, new):
    """Select tiger id to get its activity area"""
    idt = tiger_sel.value
    map_line.data = df1.query('Ind==@idt')

tiger_sel.on_change('value', tiger_line)
tiger_chart = column(tiger_sel, p)

# Output the plot to a Jupyter Notebook
curdoc().add_root(tiger_chart)
curdoc().title = "Tiger movement in Nagarahole reserve"
