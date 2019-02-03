#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go
import plotly.io as pio
import os
import numpy as np
import json
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

#print(__version__) # requires version >= 1.9.0

# cf https://plot.ly/python/getting-started/
# CGUs plotly : https://github.com/plotly/plotly.py/blob/master/LICENSE.txt

filepath = "useful_sentence_syn.json"
init_notebook_mode(connected=True)

def save_graph_image(filename, fig):
    if not os.path.exists('images'):
        os.mkdir('images')
        
    pio.write_image(fig, filename)
    
def first_graph():
    init_notebook_mode(connected=True)
       
    N = 100
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)
    sz = np.random.rand(N)*30
    
    fig = go.Figure()
    fig.add_scatter(x=x,
                    y=y,
                    mode='markers',
                    marker={'size': sz,
                            'color': colors,
                            'opacity': 0.6,
                            'colorscale': 'Viridis'
                           });
    iplot(fig)      
    save_graph_image("images/fig1.png", fig)
   

        
    

    
first_graph()    