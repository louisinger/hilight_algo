import boto3
import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import json 
import httplib2
import urllib
#import pymongo as pm

def gettopsite():
    """
    Retreive top 50 france website stats from amazon alexa
    returns : pandas dataframe
    """
    
    
    url ='https://www.alexa.com/topsites/countries/FR'
    req = requests.get(url, timeout=3)
    content = bs(req.content, "html.parser")
    tab = content.find(class_="listings table")

    type(tab)
    header = tab.find_all(class_=["th","th right"])
    h = []
    for i in header:
        h.append(i.get_text())

    h.remove('')

    header = [i.split("  ",1)[0] for i in h]

    rows = tab.find_all(class_="tr site-listing")
    r = []
    for i in rows:
        r.append(i.get_text())
    row = [re.split("\n|\n\n", i) for i in r]
    ro = [list(filter(lambda a: a!='',i)) for i in row]

    for i in ro:
        del i[2]
        del i[0]

    df = pd.DataFrame(ro, columns= header)
    return df

def getlistsite(df):
    
    """
    Retreives list of website names from dataframe got with gettopsite()
    returns: list of string
    """
    website_name = list(df.iloc[:,0])

    w = [re.split(".fr$|.com$|.ru$|.org$|.net$|.tv$",i) for i in website_name]

    for i in w:
        if (i[-1]==''):
            del i[-1]

    w.sort()

    final_site = set([i.lower() for j in w for i in j])
    final_site = [i.replace('.','') for i in final_site]
    return final_site

def apitosdr(data):
    """
    Retreive Tosdr data from api for site in data
    """
    if(isinstance(data,str)):
        u = "https://tosdr.org/api/1/service/"+data +".json"
        h = httplib2.Http()
        resp = h.request(u, 'HEAD')
        if(int(resp[0]['status']) != 200):
            return {data : "No info from tosdr"}
        else:
            with urllib.request.urlopen(u) as url:
                d = json.loads(url.read().decode())
            return {data:d}


def createdb(liste):
    """
    create dict of tosdr data
    """
    x = dict()
    for i in liste:
        x.update(apitosdr(i))
    return x

def geturl():
    """
    retreive website name and all urls from todsr dict
    """
    final_site = getlistsite(gettopsite())
    db = createdb(final_site)
    onlytosdrdb = dict((k,v) for k,v in db.items() if isinstance(v,dict))
    dictURL = dict()
    for k in onlytosdrdb.keys():
        dictURL.update({k:oui[k]['links']})
    urls = dict()
    for i,j in dictURL.items():
        dictsite = dict()
        for k,v in j.items():
            for k1,v1 in v.items():
                if k1 == 'name':
                    continue
                else:
                    dictsite.update({k:v1})
        urls.update({i:dictsite})
    return urls


def get_privacy_policies(list_of_url):   
    """
    get privacy policies from url in list
    """
    final__privacy_policy = []
    privacy_google = None #not to flood google
    for k,v in list_of_url.items():
        for k1, v1 in v.items():
            if 'privacy policy'in k1.lower():
                #print(k,k1)
                if 'google' in v1.lower():
                    if privacy_google == None :
                        privacy_google = get_text_from_html(v1)
                        final__privacy_policy.append((k, privacy_google))
                    else:
                        final__privacy_policy.append((k, privacy_google))
                else:      
                    final__privacy_policy.append((k, get_text_from_html(v1)))

    return final__privacy_policy

def get_text_from_html(url):
    '''
    convert html to text
    '''
    url = url
    req = requests.get(url, timeout=3)
    soup = bs(req.content, "html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def main_function():
    """
    function to launch to get list of tuple (webname, text)
    """
    return get_privacy_policies(geturl())



"""def connect_bdd():
    client = pm.MongoClient()
    db = client.hilight

    collection_link = db.tosl
    return collection_link"""

"""def updateDatabase():
    col = connect_bdd()
    final_site = getlistsite(gettopsite())
    test = createdb(list(final_site))
    col.drop()
    for i in test:
        if(i!= 0):
            col.insert_one(i)
"""
def lambda_handler(event, context):
    print('update the database')

