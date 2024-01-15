import pandas as pd
import numpy as np
import random

from rich.console import Console
import networkx as nx

from bokeh.plotting import figure, show, curdoc, from_network
from bokeh.models import Select, ColumnDataSource, Label, FactorRange
from bokeh.io import output_notebook, curdoc, output_file
from bokeh.layouts import row, column, gridplot
import matplotlib.pyplot as plt

df = pd.read_csv(r'data/EERecords.csv')

loc_df = pd.read_csv(r'data/EEtraplocs.csv')

cam_df = pd.read_csv(r'data/EECam_act.csv')

# Merge Dataframes
df1 = df.merge(loc_df, on='Trap_ID', how='inner')

map_line = ColumnDataSource(df1)

df1['Ind'] = df1['Ind'].apply(lambda x: str(x))

df_pivot = df1[['Ind','Trap_ID']].value_counts().reset_index()

df_pivot.columns = ['Ind', 'Trap_ID', 'count']

count_line = ColumnDataSource(df_pivot)

locs = list(df['Trap_ID'].unique())

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
# p.scatter(
#     source=map_line,
#     x='CenteredX',
#     y='CenteredY',
#     size=10,
#     alpha=0.5
# )

#Choose a title!
title = 'Les Miserables character network'

#Choose colors for node and edge highlighting
node_highlight_color = 'white'
edge_highlight_color = 'black'

#Choose attributes from G network to size and color by — setting manual size (e.g. 10) or color (e.g. 'skyblue') also allowed
color_by_this_attribute = 'modularity_color'

#Pick a color palette — Blues8, Reds8, Purples8, Oranges8, Viridis8
color_palette = Reds8

#Establish which categories will appear when hovering over each node
HOVER_TOOLTIPS = [("Character","@index"),
                  ("Modularity Class", "@modularity_class"),]

#Create a plot — set dimensions, toolbar, and title

plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset",
              active_scroll='wheel_zoom',
              x_range=Range1d(-10.1, 10.1),
              y_range=Range1d(-10.1, 10.1),
              title=title)

#Create a network graph object with spring layout
# https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
network_graph = from_networkx(G, nx.circular_layout, scale=10, center=(0, 0))

#Set node sizes and colors according to node degree (color as category from attribute)
network_graph.node_renderer.glyph = Circle(size=15, fill_color=color_by_this_attribute)

#Set edge opacity and width
network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

#Add Labels
x, y = zip(*network_graph.layout_provider.graph_layout.values())
node_labels = list(G.nodes())
source = ColumnDataSource({'x': x,
                           'y': y,
                           'name': [node_labels[i] for i in range(len(x))]})
labels = LabelSet(x='x',
                  y='y',
                  text='name',
                  source=source,
                  text_font_size='10px',
                  background_fill_color='white',
                  background_fill_alpha=.7)
plot.renderers.append(labels)

#Add network graph to the plot
plot.renderers.append(network_graph)

#output_notebook()
#Show the plot
#show(plot)

# p.line(
#     source=map_line,
#     x='CenteredX',
#     y='CenteredY',
#     line_width=2,
#     color='red',
#     legend_label="Tiger's path"
# )

# Add a heatmap to recognize tiger presence in the area (camera trap)
h = figure(
    plot_width=700,
    plot_height=400,
    title="Appearances",
    y_range=count_line
)

h.hbar(
    source=count_line,
    y='Trap_ID',
    left='count',
    right=0,
    fill_color="orange",
    height=0.9
)

# Function
def tiger_line(attr, old, new):
    """Select tiger id to get its activity area"""
    idt = tiger_sel.value
    map_line.data = df1.query('Ind==@idt').groupby(['Ind', 'Trap_ID', 'CenteredX', 'CenteredY'])
    count_line = df_pivot.query('Ind==@idt').groupby('Trap_ID') 
    # count_line.y_range = df_pivot.query('Ind==@idt')['Trap_ID']

# Change using dropdown
tiger_sel.on_change('value', tiger_line)
tiger_chart = row(column(tiger_sel, p), h)

# Output the plot to a dashboard
curdoc().add_root(tiger_chart)
curdoc().title = "Tiger movement in Nagarahole reserve"