import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import os
import numpy as np
import json
from pprint import pprint
import  requests
from collections import Counter

plotly.tools.set_credentials_file(username='axelc', api_key='6qQk1TZYuAOpw0g7smjc')

#construit le dictionnaire des mots et leur occurence(plus tard faire par importance)
def build_dic():
    #on récupère les données qu'on a auparavant analysées
    f = open('useful_sentence_syn.json')
    cgu = json.load(f)
    
    dic = {}
    for data in cgu:
        for key,value in data.items():
            for word in value[0]:
                if not word in dic:
                    dic[word] = 1
                else:
                    dic[word] += 1
    return dic

def graph_bar():
    dic = build_dic() 

    #on parcourt le dic pour le transformer en graphe
    dataBar = []
    for word in dic:
        trace = go.Bar(
            x=[word],
            y=[dic[word]],
            name=word
        )
        dataBar.append(trace)
        
    py.plot(dataBar, filename = 'twitter-basic-bar', auto_open=True)


def graph_pie():
    dic = build_dic() 
    labels = []
    values = []
    
    #dataPie = []
    for word in dic:
        labels.append(word)
        values.append(dic[word])

    trace = go.Pie(labels=labels, values=values)
    py.plot([trace], filename = 'twitter-basic-pie', auto_open=True)

graph_bar()
graph_pie()
    



