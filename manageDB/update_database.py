import boto3

def gettopsite():
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

    if(isinstance(data,str)):
        a = 0
        u = "https://tosdr.org/api/1/service/"+data +".json"
        h = httplib2.Http()
        resp = h.request(u, 'HEAD')
        if(int(resp[0]['status']) != 200):
            return 0
        else:
            a = a+1
            print(a)
            with urllib.request.urlopen(u) as url:
                d = json.loads(url.read().decode())
            return d


def createdb(liste):
    x = []
    for i in liste:
        x.append(apitosdr(i))
    return x

def connect_bdd():
    client = pm.MongoClient()
    db = client.hilight

    collection_link = db.tosl
    return collection_link

def updateDatabase():
    col = connect_bdd()
    final_site = getlistsite(gettopsite())
    test = createdb(list(final_site))
    col.drop()
    for i in test:
        if(i!= 0):
            col.insert_one(i)

def lambda_handler(event, context):
    print('update the database')