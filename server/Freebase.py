import json
import urllib.request
import urllib.parse
import re
import Proxy
import subprocess
import datetime
import Config

#code:
#0:ok
#1:plusieurs options possibles
#2:pas trouve
#verification du type

global lfilter
#patern,filtre|filtre2
lfilter=[
#personne\
"(date|annee).*naissance","/people/person/date_of_birth",\
"metier|profession","/people/person/profession",\
"nationalite|origine|originaire","/people/person/nationality",\
"sexe|genre","/people/person/gender",\
"masse|poids","/people/person/weight_kg",\
"taille","/people/person/height_meters",\
"(date|annee).*deces","/people/deceased_person/date_of_death",\
#geographie\
"code.*postale","/location/citytown/postal_codes"
"population|(nombre.*habitants)","/location/statistical_region/population",\
#chimie\
"masse.*atomique","/chemistry/chemical_element/atomic_mass",\
"nombre.*atomique","/chemistry/chemical_element/atomic_number",\
"symbole.*","/chemistry/chemical_element/symbol|chemistry/chemical_compound/formula",\
"formule.*","/chemistry/chemical_compound/formula",\
"temperature.*fusion","/chemistry/chemical_element/melting_point|/chemistry/chemical_compound/melting_point",\
"temperature.*ebullition","/chemistry/chemical_element/boiling_point|/chemistry/chemical_compound/boiling_point"\
]

global api_key
global service_url
global service_url2
global defaultResponse
defaultResponse=Config.defaultFreebaseResponse
api_key=Config.api_key
service_url=Config.service_url
service_url2=Config.service_url2

def searchTopic(top,input):
    global api_key
    global service_url
    liste=[]
    res="J'ai trouvé plusieurs résultats possibles, lequel convient:\n"
    params = {
        'query': top,
        'limit': 10,
        'indent': "true",
        'key': api_key,
        'lang' : 'fr'
    }

    url = service_url + '?' + urllib.parse.urlencode(params)
    response = json.loads(urllib.request.urlopen(url).read().decode('utf-8','ignore'))
    i=0
    for result in response['result']:
        top1=top.replace("_"," ")
        if re.search(top,str(result)):
            if result['name'].lower()==top1 or result['id']=="/en/"+top:    
                res+=str(i)+") "+result['name']+";("+result['id']+")\n"
                liste.append(result['mid'])
                i+=1
        elif re.search(input,str(result)):
            if result['name'].lower()==input.lower():
                res+=str(i)+") "+result['name']+";("+result['id']+")\n"
                liste.append(result['mid'])
                i+=1                
    return res.strip(),liste

def searchInfos(top,fil):
    global api_key
    global service_url2
    global defaultResponse
    rep=""
    topic_id = top
    params = {
        'key': api_key,
        'filter': fil,
        'indent': "true",
        'lang': 'fr'
    }
    url = service_url2 + topic_id + '?' + urllib.parse.urlencode(params)
    try:
        page=urllib.request.urlopen(url).read().decode('utf-8','ignore')
        topic = json.loads(page)
        for property in topic['property']:
            if topic['property'][property]['valuetype']=='compound':
                for value in topic['property'][property]['values']:
                    temp=value['text'].split(' - ')
                    rep=temp[0]
                    break
            else:
                for value in topic['property'][property]['values']:
                    rep+=value['text']+" "
        code=0
    except:
        rep=defaultResponse
        code=2
    return code,rep

def search(code=0,phrase="",infos=[]):
    global defaultResponse
    global lfilter
    filter,top,rep,res="","","",""
    phrase=phrase[:1].lower()+phrase[1:]#retrait de la majuscule de debut de phrase
    if code==0:
        i,possible=0,0
        while i < len(lfilter):
            if re.search(lfilter[i],phrase):
                m=re.search(lfilter[i],phrase)
                temp=m.group(0).split(" ")
                if len(temp)>possible:
                    possible=len(temp)
                    filter=lfilter[i+1]
            i+=2
        m=re.search("[A-Z].*[a-z]",phrase)#recherche mieux
        topic=m.group(0)
        topic=topic.replace("ç","c")
        topic=topic.replace("à","a")
        topic=topic.replace("é","e")
        topic=topic.replace("è","e")
        topic=topic.replace("ù","u")
        input=topic
        topic=topic.replace(" ","_")
        topic=topic.lower()
        res,liste=searchTopic(topic,input)#recherche des topics possibles
        if len(liste)==1:#si un seul trouve, on cherche la reponse
            top=liste[0]
            if not re.search("|",filter):
                code,rep=searchInfos(top,filter)
            else:#si plusieurs filtre possible on cherche le 1er puis le 2ème.
                t=filter.split("|")
                filter=t[0]
                code,rep=searchInfos(top,filter)
                if re.search("Impossible",rep):
                    filter=t[1]
                    code,rep=searchInfos(top,filter)
        elif len(liste)>1:
            res=res.replace("_"," ")
            res=res.replace(";","")
            res=res.replace("/en/","")
            rep=res
            code=1
            top=liste
        else:
            rep=defaultResponse
            code=2
    else:#code==1
        liste=infos[2]
        filter=infos[3]
        top=liste[int(phrase)]
        code,rep=searchInfos(top,filter)
        top,filter,topic="","",""
    infos=["freebase",code,top,filter,"Freebase.search"]
    return rep,infos

"""Proxy.connectProxy('https')
code=0
i=[]
while 1:
    phrase=input('>')
    if phrase=="quit":
        quit()
    e,i=search(code,phrase,i)
    code=i[1]
    print(e)
"""
