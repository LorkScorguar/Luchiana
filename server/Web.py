#!/usr/bin/python3.3

"""
ID TABLEAU DONNEES WIKIPEDIA
0 : Ville
0 : Telephone
0 : Architecture
0 : Personnalite
0 : Film
0 : Bateau
3 : Element chimique
+1 : si bandeau en tableau indiquant modif de l'article à faire (ex: linux)
+1 : si bandeau en tableau indiquant la présence d'homonymie (ex: google)

FONCTIONS:
-translation de mot:
    Réalisation=réalisateur,cinéaste
    Masse=poids
    Dimensions=taille
    Créé par/Scénario=auteur,dessinateur
    Pays:origines
+gestion homonymes: proposer les différents choix et en retenir les urls
-gestion urls complexes: faire recherche et proposer les choix et retenir les urls
-multiple backends: wikipedia, google, etc

ERREURS:
+Demander le département d'une ville
+problème avec les urls en UTF-8+
+absence de th sur certaines pages (ex:Tintin)

A TESTER:
utiliser http://fr.mobile.wikipedia.org/ pour plus de rapidite
"""

import urllib.request
import re
import ssl
import json
import datetime
import xml.etree.ElementTree as ET

import Config

def demandeChoix(page):
    start=page.find("<ul>")
    end=page.find("</ul>")
    infos=page[start:end]
    rep=[]
    url=""
    temp=infos.split("</li>\n")
    for i in range(len(temp)):
        p = re.compile(r'\" title.*$')
        url = p.sub('',temp[i])
        p = re.compile(r'<ul>\n')
        url = p.sub('',url)
        p = re.compile(r'<li><a href=\"/wiki/')
        url = p.sub('',url)
        rep.append(url)#ajout de l'url wiki associee au nom
    rep2 = [x for x in rep if x]
    return rep2

def getWikiInfos(texte):#ne recup que les infos du cadre à droite de wikipedia
    texte = urllib.request.quote(texte)
    p = re.compile(r'25')#permet de supprimer les 25 qui s'interale dans les urls déjà converties
    texte = p.sub('',texte)
    url = "http://fr.wikipedia.org/wiki/"+texte
    site = urllib.request.Request(url)
    site.add_header("User-Agent","Luchiana v3")
    page = urllib.request.urlopen(site).read().decode('utf-8','ignore')
    start=page.find("<!-- bodycontent -->")
    end=page.find("Sommaire")
    infos=page[start:end]
    return infos

def getData(texte,typeInfo):
    error=""
    quest=""
    fct="Web.getData"
    data=""
    res=""
    codeErreur=0
    ltypeInfo=typeInfo.split(" ")
    infos=getWikiInfos(texte)
    search="ok"
    if re.search("Cette page d’<a href=\"/wiki/Aide:Homonymie\" title=\"Aide:Homonymie\">homonymie</a> répertorie les différents sujets et articles partageant un même nom.",infos):
        codeErreur=0
        error="homonymie"
        search="non"
        rep=demandeChoix(infos)
        quest="Plusieurs choix correspondent à votre demande: "+texte
        mrep=""
        i=0
        while i < len(rep):
            mrep+=str(i)+"-"+str(rep[i])+"\n"
            i=i+1
        quest=quest+"\nQuel est votre choix?\n"+mrep
    if search=="ok":
        itab=0
        if re.search("bandeau-titre",infos):
            itab=itab+infos.count("bandeau-titre")
        tableau=infos.split("</table")
        ligne=tableau[itab].split("</tr>\n<tr>")
        for i in range(len(ligne)):
            e=0
            for j in range(len(ltypeInfo)):
                if re.search(ltypeInfo[j]+"[<|\b*]",ligne[i],flags=re.IGNORECASE):
                    e=e+1
                if e == len(ltypeInfo):
                    res=ligne[i]
        try:
            temp=res.split("</th>\n<td")
            p = re.compile(r'<.*?>')
            data = p.sub('',temp[1])
        except:
            temp=res.split("</td>\n<td")
            p = re.compile(r'<.*?>')
            data = p.sub('',temp[1])
        p2 = re.compile(r'\[.*?\]')
        data = p2.sub('',data)
        p3 = re.compile(r'\(.*?\)')
        data = p3.sub('',data)
        p4 = re.compile(r'&#[0-9]{3};')
        data = p4.sub(' ',data)
        p5 = re.compile(r'.*?>')
        data = p5.sub(' ',data)
        codeErreur=1
        if re.search("hab.",data.strip()):
            res=data.strip()[:-5]
        else:
            res=data.strip()
    return codeErreur,error,quest,fct,res

"""nom=input("Entrer le nom de ce sur quoi vous voulez des infos: ")
typeInfo=input("Entrer le type d'info voulu: ")
res=getData(nom,typeInfo)
print(res[1])
"""


def ignoreCertificate():
    context = ssl.create_default_context()
    context.check_hostname=False
    context.verify_mode = ssl.CERT_NONE
    return context

def getBtcValue():
    context=ignoreCertificate
    url="http://api.bitcoincharts.com/v1/weighted_prices.json"
    req=urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    context=ignoreCertificate()
    resp=urllib.request.urlopen(req,context=context)
    jResp=json.loads(resp.read().decode('utf-8'))
    infos=["web",0,"Web.getBtcValue"]
    return jResp['EUR']['24h'],infos

def getMoneroValue():
    price=0
    context=ignoreCertificate
    url="https://coinmarketcap.com/#EUR"
    req=urllib.request.Request(url)
    context=ignoreCertificate()
    resp=urllib.request.urlopen(req,context=context)
    data=resp.read().decode('utf-8')
    rates=data.split("<div id=\"currency-exchange-rates\"")[1]
    rates=rates.split("></div>")[0]
    lrate=rates.split("\n")
    for item in lrate:
        if re.search("eur",item):
            rate=item.split("=")[1]
            rate=rate.replace("\"","")
    data=data.split("<table class=\"table\" id=\"currencies\">")[1]
    data=data.split("</table>")[0]
    currencies=data.split("<tr id=")
    del currencies[0]#remove table headers
    for currency in currencies:
        if "id-monero" in currency:
            tmp=currency.split("class=\"price\"")[1]
            tmp=tmp.split("data-btc")[0]
            m=re.search("\d*\.\d*",tmp)
            price=float(m.group(0))/float(rate)
    infos=["web",0,"Web.getMoneroValue"]
    return price,infos

def getWeather(message):
    res=""
    r=re.findall("[A-Z][a-z]*",message)
    city=r[len(r)-1]
    apikey=Config.weather_apikey
    url="http://api.openweathermap.org/data/2.5/weather?APPID="+apikey+"&lang=fr&units=metric&q="+city
    req=urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    context=ignoreCertificate()
    resp=urllib.request.urlopen(req,context=context)
    jResp=json.loads(resp.read().decode('utf-8'))
    #print(jResp)
    res="La météo à "+city+" est "+str(jResp['weather'][0]['description'])+" ("+str(jResp['main']['temp_min'])+"°C-"+str(jResp['main']['temp_max'])+"°C)"
    infos=["web",0,"Web.getWeather"]
    return res,infos

def getTomorrowWeather(message):
    res=""
    r=re.findall("[A-Z][a-z]*",message)
    city=r[len(r)-1]
    apikey=Config.weather_apikey
    url="http://api.openweathermap.org/data/2.5/forecast?APPID="+apikey+"&lang=fr&units=metric&q="+city
    req=urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    context=ignoreCertificate()
    resp=urllib.request.urlopen(req,context=context)
    jResp=json.loads(resp.read().decode('utf-8'))
    today=datetime.datetime.now()
    tomorrow=today+datetime.timedelta(days=1)
    dweather={}
    ltemp=[]
    for item in jResp['list']:
        if re.search(tomorrow.strftime("%Y-%m-%d"),item['dt_txt']):
            if item['weather'][0]['description'] not in dweather.keys():
                dweather[item['weather'][0]['description']]=1
            else:
                dweather[item['weather'][0]['description']]+=1
            ltemp.append(item['main']['temp_min'])
            ltemp.append(item['main']['temp_max'])
    weather=max(dweather,key=dweather.get)
    temp_min=min(ltemp)
    temp_max=max(ltemp)
    res="Demain, la météo à "+city+" sera "+str(weather)+" ("+str(temp_min)+"°C-"+str(temp_max)+"°C)"
    infos=["web",0,"Web.getTomorrowWeather"]
    return res,infos

def rssParse(url):
    req=urllib.request.Request(url)
    context=ignoreCertificate()
    resp=urllib.request.urlopen(req,context=context)
    data=resp.read().decode('utf-8')
    root=ET.fromstring(data)
    darticles={}
    site=""
    if url.split(".")[1]!="feedburner":
        site=url.split(".")[1]
    else:
        site=url.split("/")[-1]
    for item in root[0]:
        if item.tag=="item":
            #title=description;data;link
            darticles[item[0].text+"("+site+")"]=item[1].text+";"+item[2].text+";"+item[3].text
    return darticles

def checkNews():
    interestingNews={}
    for url in Config.news_url:
        darticles=rssParse(url)#get recent articles for each website
        for k,v in darticles.items():
            for topic in Config.topics:
                if re.search(topic,k,re.IGNORECASE) or re.search(topic,v,re.IGNORECASE):#if we found the topic, then article is interesting
                    interestingNews[k]=v
    for k,v in interestingNews.items():
        print(k)
    return "ok"

def checkKorben():
    url="https://korben.info/feed"
    darticles=rssParse(url)
    for k, v in darticles.items():
        print(k)
    return "ok"

def checkFrandroid():
    url="http://www.frandroid.com/feed"
    darticles=rssParse(url)
    for k, v in darticles.items():
        print(k)
    return "ok"

def checkPhonandroid():
    url="http://www.phonandroid.com/feed"
    darticles=rssParse(url)
    for k, v in darticles.items():
        print(k)
    return "ok"

def checkXda():
    url="http://xda-developers.com/news.rss"
    darticles=rssParse(url)
    for k, v in darticles.items():
        print(k)
    return "ok"

def checkLinuxFR():
    journaux="http://linuxfr.org/journaux.atom"
    news="http://linuxfr.org/news.atom"
    return "ok"

def checkReddit(subreddit):
    return "ok"

checkNews()
