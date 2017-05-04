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
-gestion urls complexes: faire recherche et proposer les choix
 et retenir les urls
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
    """Fonction pour demander à un choix à l'utilisateur si plusieurs pages
    correspondent"""
    start = page.find("<ul>")
    end = page.find("</ul>")
    infos = page[start:end]
    rep = []
    url = ""
    temp = infos.split("</li>\n")
    for i in range(len(temp)):
        regex = re.compile(r'\" title.*$')
        url = regex.sub('', temp[i])
        regex = re.compile(r'<ul>\n')
        url = regex.sub('', url)
        regex = re.compile(r'<li><a href=\"/wiki/')
        url = regex.sub('', url)
        rep.append(url)#ajout de l'url wiki associee au nom
    rep2 = [x for x in rep if x]
    return rep2

def getWikiInfos(texte):
    """Fonction de récupération des informations en encadré sur les pages
    Wikipédia"""
    texte = urllib.request.quote(texte)
    #permet de supprimer les 25 qui s'intercalent dans les urls déjà converties
    regex = re.compile(r'25')
    texte = regex.sub('', texte)
    url = "http://fr.wikipedia.org/wiki/"+texte
    site = urllib.request.Request(url)
    site.add_header("User-Agent", "Luchiana v3")
    page = urllib.request.urlopen(site).read().decode('utf-8', 'ignore')
    start = page.find("<!-- bodycontent -->")
    end = page.find("Sommaire")
    infos = page[start:end]
    return infos

def getData(texte, typeInfo):
    """Fonction de récupération des données d'une page Wikipédia"""
    error = ""
    quest = ""
    fct = "Web.getData"
    data = ""
    res = ""
    codeErreur = 0
    ltypeInfo = typeInfo.split(" ")
    infos = getWikiInfos(texte)
    search = "ok"
    if re.search(r"Cette page d’<a href=\"/wiki/Aide:Homonymie\" "\
                  "title=\"Aide:Homonymie\">homonymie</a> "\
                  "répertorie les différents sujets et articles "\
                  "partageant un même nom.", infos):
        codeErreur = 0
        error = "homonymie"
        search = "ko"
        rep = demandeChoix(infos)
        quest = "Plusieurs choix correspondent à votre demande: "+texte
        mrep = ""
        i = 0
        while i < len(rep):
            mrep += str(i)+"-"+str(rep[i])+"\n"
            i = i+1
        quest = quest+"\nQuel est votre choix?\n"+mrep
    if search == "ok":
        itab = 0
        if re.search("bandeau-titre", infos):
            itab = itab+infos.count("bandeau-titre")
        tableau = infos.split("</table")
        ligne = tableau[itab].split("</tr>\n<tr>")
        for i in range(len(ligne)):
            k = 0
            for j in range(len(ltypeInfo)):
                if re.search(ltypeInfo[j]+"[<|\b*]", ligne[i], re.IGNORECASE):
                    k = k+1
                if k == len(ltypeInfo):
                    res = ligne[i]
        try:
            temp = res.split("</th>\n<td")
            regex = re.compile(r'<.*?>')
            data = regex.sub('', temp[1])
        except:
            temp = res.split("</td>\n<td")
            regex = re.compile(r'<.*?>')
            data = regex.sub('', temp[1])
        regex = re.compile(r'\[.*?\]')
        data = regex.sub('', data)
        regex = re.compile(r'\(.*?\)')
        data = regex.sub('', data)
        regex = re.compile(r'&#[0-9]{3};')
        data = regex.sub(' ', data)
        regex = re.compile(r'.*?>')
        data = regex.sub(' ', data)
        codeErreur = 1
        if re.search("hab.", data.strip()):
            res = data.strip()[:-5]
        else:
            res = data.strip()
    return codeErreur, error, quest, fct, res

#nom=input("Entrer le nom de ce sur quoi vous voulez des infos: ")
#typeInfo=input("Entrer le type d'info voulu: ")
#res=getData(nom,typeInfo)
#print(res[1])



def ignoreCertificate():
    """Fonction outil pour ne pas vérifier les certificats ssl"""
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

def getBtcValue():
    """Récupére la valeur en euro d'un Bitcoin"""
    contex = ignoreCertificate
    url = "http://api.bitcoincharts.com/v1/weighted_prices.json"
    req = urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    contex = ignoreCertificate()
    resp = urllib.request.urlopen(req, context=contex)
    jResp = json.loads(resp.read().decode('utf-8'))
    infos = ["web", 0, "Web.getBtcValue"]
    return jResp['EUR']['24h'], infos

def getMoneroValue():
    """Récupére la valeur en euro d'un Monero"""
    price = 0
    contex = ignoreCertificate
    url = "https://coinmarketcap.com/#EUR"
    req = urllib.request.Request(url)
    contex = ignoreCertificate()
    resp = urllib.request.urlopen(req, context=contex)
    data = resp.read().decode('utf-8')
    rates = data.split("<div id=\"currency-exchange-rates\"")[1]
    rates = rates.split("></div>")[0]
    lrate = rates.split("\n")
    for item in lrate:
        if re.search("eur", item):
            rate = item.split("=")[1]
            rate = rate.replace("\"", "")
    data = data.split("<table class=\"table\" id=\"currencies\">")[1]
    data = data.split("</table>")[0]
    currencies = data.split("<tr id=")
    del currencies[0]#remove table headers
    for currency in currencies:
        if "id-monero" in currency:
            tmp = currency.split("class=\"price\"")[1]
            tmp = tmp.split("data-btc")[0]
            regex = re.search(r"\d*\.\d*", tmp)
            price = float(regex.group(0))/float(rate)
    infos = ["web", 0, "Web.getMoneroValue"]
    return price, infos

def getWeather(message):
    """Récupére la météo du jour"""
    res = ""
    regex = re.findall("[A-Z][a-z]*", message)
    city = regex[len(regex)-1]
    url = "http://api.openweathermap.org/data/2.5/weather?APPID="+\
          Config.weather_apikey+\
          "&lang=fr&units=metric&q="+city
    req = urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    contex = ignoreCertificate()
    resp = urllib.request.urlopen(req, context=contex)
    jResp = json.loads(resp.read().decode('utf-8'))
    #print(jResp)
    res = "La météo à "+city+" est "+str(jResp['weather'][0]['description'])+\
          " ("+str(jResp['main']['temp_min'])+"°C-"+\
          str(jResp['main']['temp_max'])+"°C)"
    infos = ["web", 0, "Web.getWeather"]
    return res, infos

def getTomorrowWeather(message):
    """Récupére la météo du lendemain"""
    regex = re.findall("[A-Z][a-z]*", message)
    city = regex[len(regex)-1]
    url = "http://api.openweathermap.org/data/2.5/forecast?APPID="+\
          Config.weather_apikey+"&lang=fr&units=metric&q="+city
    req = urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    contex = ignoreCertificate()
    resp = urllib.request.urlopen(req, context=contex)
    jResp = json.loads(resp.read().decode('utf-8'))
    tomorrow = datetime.datetime.now()+datetime.timedelta(days=1)
    dweather = {}
    ltemp = []
    for item in jResp['list']:
        if re.search(tomorrow.strftime("%Y-%m-%d"), item['dt_txt']):
            if item['weather'][0]['description'] not in dweather.keys():
                dweather[item['weather'][0]['description']] = 1
            else:
                dweather[item['weather'][0]['description']] += 1
            ltemp.append(item['main']['temp_min'])
            ltemp.append(item['main']['temp_max'])
    weather = max(dweather, key=dweather.get)
    res = "Demain, la météo à "+city+" sera "+str(weather)+\
          " ("+str(min(ltemp))+"°C-"+str(max(ltemp))+"°C)"
    infos = ["web", 0, "Web.getTomorrowWeather"]
    return res, infos

def rssParse(url):
    """Simple parser de RSS"""
    req = urllib.request.Request(url)
    contex = ignoreCertificate()
    req.add_header("User-Agent", "Luchiana 3.0")
    resp = urllib.request.urlopen(req, context=contex)
    data = resp.read().decode('utf-8')
    root = ET.fromstring(data)
    darticles = {}
    site = ""
    if re.search("feedburner", url):
        site = url.split("/")[-1]
    elif re.search("www", url):
        site = url.split(".")[1]
    else:
        site = url.split(".")[0]
        site = site.split("//")[1]
    if re.search("atom", url):
        for item in root:
            if item.tag == "{http://www.w3.org/2005/Atom}entry":
                #title=description;date;link
                darticles[item.find("{http://www.w3.org/2005/Atom}title").text+\
                "("+site+")"] = \
                item.find("{http://www.w3.org/2005/Atom}content").text+";"+\
                item.find("{http://www.w3.org/2005/Atom}published").text+";"+\
                item.find("{http://www.w3.org/2005/Atom}link").attrib['href']
    else:
        for item in root[0]:
            if item.tag == "item":
                #title=description;date;link
                darticles[item.find('title').text] = site+";"+\
                item.find('description').text+";"+item.find('pubDate').text+\
                ";"+item.find('link').text
    return darticles

def checkNews():
    """Récupére toutes les news et retournent celles intéressantes"""
    dinterestingNews = {}
    try:
        fich = open("database/previous_web", "r")
        for line in fich:
            if re.search("reddit", line):
                redd = line.split("=")[1]
            if re.search("web", line):
                web = line.split("=")[1]
        fich.close()
    except FileNotFoundError:
        redd = ""
        web = ""
    fich = open("database/previous_web", "w")
    fich.write("reddit="+redd+"\r\n")
    viewed = []
    for url in Config.news_url:
        darticles = rssParse(url)#get recent articles for each website
        for k, v in darticles.items():
            for topic in Config.topics:
                if re.search(topic, k, re.IGNORECASE) or re.search(topic, v, re.IGNORECASE):
                    if k.strip() not in web.split(";,;"):
                        dinterestingNews[k] = v
                    viewed.append(k.strip())
    fich.write("web="+";,;".join(viewed)+"\r\n")
    fich.close()
    res = ""
    for k, v in dinterestingNews.items():
        res += k+" ("+v.split(";")[0]+")\r\n"
    infos = ["web", 0, "Web.checkNews"]
    return res, infos

def getReddit(subreddit):
    """Fonction de récupération des tous les topics d'un subbreddit"""
    url = "https://www.reddit.com/r/"+subreddit+".json"
    req = urllib.request.Request(url)
    req.add_header("content-type", "application/json")
    req.add_header("User-Agent", "Luchiana 3.0")
    contex = ignoreCertificate()
    resp = urllib.request.urlopen(req, context=contex)
    jResp = json.loads(resp.read().decode('utf-8'))
    darticles = {}
    for item in jResp['data']['children']:
        title = str(item['data']['title'])
        url = str(item['data']['url'])
        description = str(item['data']['selftext'])
        date = str(item['data']['created_utc'])
        darticles[title] =  subreddit+";"+description+";"+date+";"+url
    return darticles

def checkReddit():
    """fonction de récupération des topics intéressants"""
    dinterestingReddit = {}
    try:
        fich = open("database/previous_web", "r")
        for line in fich:
            if re.search("reddit", line):
                redd = line.split("=")[1]
            if re.search("web", line):
                web = line.split("=")[1]
        fich.close()
    except FileNotFoundError:
        redd = ""
        web = ""
    fich = open("database/previous_web", "w")
    fich.write("web="+web+"\r\n")
    viewed = []
    for sub in Config.reddit:
        darticles = getReddit(sub)
        for k, v in darticles.items():
            if k.strip() not in redd.split(";,;"):
                dinterestingReddit[k] = v
            viewed.append(k.strip())
    fich.write("reddit="+";,;".join(viewed)+"\r\n")
    fich.close()
    res = ""
    for k, v in dinterestingReddit.items():
        res += k+" (r/"+v.split(";")[0]+")\r\n"
    infos = ["web", 0, "Web.checkReddit"]
    return res, infos

if __name__ == '__main__':
    cnews = checkNews()
    creddit = checkReddit()
    print(cnews)
    print(creddit)
