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

categories = ["Personal data", "data controller", "Log data", "account data", "Processing", "third parties", "profiling", 
"Data Subject", "Data Protection Officer", "Data Protection Authority"]

#construit le dictionnaire des mots et leur occurence(grouped words)
def build_dic_full():
    #on récupère les données qu'on a auparavant analysées
    f = open('useful_sentence_full.json')
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


#construit le dictionnaire des mots et leur occurence(basic words)
def build_dic_basic():
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
    dic_full = build_dic_full() 

    #on parcourt le dic pour le transformer en graphe
    dataBar = []
    for word in dic_full:
        trace = go.Bar(
            x=[word],
            y=[dic_full[word]],
            name=word
        )
        dataBar.append(trace)
        
    py.plot(dataBar, filename = 'twitter-bar-basic', auto_open=True)

    dic_basic = build_dic_basic() 

    #on parcourt le dic pour le transformer en graphe
    dataBar = []
    for word in dic_basic:
        trace = go.Bar(
            x=[word],
            y=[dic_basic[word]],
            name=word
        )
        dataBar.append(trace)
        
    py.plot(dataBar, filename = 'twitter-bar-grouped', auto_open=True)


def graph_pie():
    dic_full = build_dic_full() 
    labels = []
    values = []
    
    for word in dic_full:
        labels.append(word)
        values.append(dic_full[word])

    trace = go.Pie(labels=labels, values=values)
    py.plot([trace], filename = 'twitter-pie-grouped', auto_open=True)


    dic_basic = build_dic_basic()
    labels = []
    values = []
    
    for word in dic_basic:
        labels.append(word)
        values.append(dic_basic[word])

    trace = go.Pie(labels=labels, values=values)
    py.plot([trace], filename = 'twitter-pie-basic', auto_open=True)

def json_grade_test():
    from random import randint
    data = {}
    for categ in categories:
        data[categ] = randint(-1,1)

    json_data = json.dumps(data)

    with open('json_grade_test.json', 'w') as outfile:
        json.dump(data, outfile)

    return json_data


def compare_grade_percentage():
    grades = json.loads(json_grade_test())
    dic = build_dic_full()

    #on parcourt les data pour évaluer l'importance de chaque
    data_evaluation_bad = {}
    data_evaluation_good = {}

    for key in categories:
        if grades[key] == -1:
            data_evaluation_bad[key] = dic[key]
        elif grades[key] == 0:
            data_evaluation_bad[key] = dic[key]/2
            data_evaluation_good[key] = dic[key]/2
        else:
            data_evaluation_good[key] = dic[key]


    dataBar_bad = []
    for word in data_evaluation_bad:
        trace = go.Bar(
            x=[word],
            y=[data_evaluation_bad[word]],
            name=word
        )
        dataBar_bad.append(trace)

    dataBar_good = []
    for word in data_evaluation_good:
        trace = go.Bar(
            x=[word],
            y=[data_evaluation_good[word]],
            name=word
        )
        dataBar_good.append(trace)    

    py.plot(dataBar_bad, filename = 'twitter-bad-bar', auto_open=True)
    py.plot(dataBar_good, filename = 'twitter-good-bar', auto_open=True)
    

#graph_bar()
#graph_pie()
compare_grade_percentage()



