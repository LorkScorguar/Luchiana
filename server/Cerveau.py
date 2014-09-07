#Modules de base
import re
import datetime
import subprocess
from random import choice

#Modules specifiques
import Proxy
import Freebase
import System
import Math
import Mail
import Config
import FileManager

global infos
global action 
global code
global reponse
global listeFichiers
reponse=Config.defaultResponse
listeFichiers=Config.listeFichiers
infos=[]
code=0
action="" 


Articles=["le","la","les","l","un","une","des","du"]
PronomsSujet=["j","je","tu","il","elle","on","nous","vous","ils","elles"]
PronomsPossessif=["mon","ton","son","ma","ta","sa","mes","tes","ses"]    
Question=["comment","quel","quelle","quand","combien","qui","que","qu'est-ce","qu'est ce"]
Ponctuation=[".","!","?","...",",",";",":","(",")"]

def init():
    global dico
    dico=[]
    dic=open("dico/dico-fr.txt","r")
    for line in dic:
        dico.append(line.strip())


def analyse(phrase,username):
    global action
    global code
    global infos
    global reponse
    type=""
    resIn,resOut="",""
    act,typeAct,rep="","",""
    if re.search("[A-Z].*",phrase):
        m=re.search("[A-Z].*",phrase)
        resIn=m.group(0)
    if action=="":#gestion passage initial
        if re.search("(calcul|combien|pythagore|thales|perimetre|surface|volume|triangle)?[-+]?\d+",phrase,re.IGNORECASE) or re.search("([-+]?\d+)+",phrase):
        #if re.search("toto",phrase):
            if re.search("[triangle,rectangle]",phrase,re.IGNORECASE):
                phrase+=" pythagore"
            type="T"
            rep=Math.run(phrase)
        else:
            possible=0
            for file in listeFichiers:
                fichier=open("database/"+file,"r")
                for ligne in fichier:
                    temp=ligne.split(";")
                    mots=temp[0]
                    i=0
                    while i < len(mots):
                        if re.search(mots,phrase,re.IGNORECASE):
                            t=mots.split(".*")
                            if len(t)>possible:
                                possible=len(t)
                                typeAct=temp[1]
                                act=temp[2]
                                reponse=temp[3]
                        i+=2
            type="T"
            listRep=reponse.split("/")
            rep=choice(listRep)

            #remplacement du %IN% dans l'action
            listeAct=act.split(" ")
            for i in range(len(listeAct)):
                if listeAct[i].strip()=="%IN%":
                    #listeAct[i]="'"+resIn.strip()+"'"
                    listeAct[i]="'"+phrase.strip()+"'"
            act=" ".join(listeAct)
            if typeAct=="bash":#récupération des infos en plus
                if re.search("%OUT%",reponse):
                    resOut=subprocess.check_output(act,shell=True)
                else:
                    resOut=System.command(act)
            elif typeAct=="python":
                resOut,infos=eval(act)
                action=infos[0]
                code=infos[1]

            listeMot=rep.split(" ")
            #remplacement des %IN% et %OUT% dans la réponse
            if typeAct!="python" or (typeAct=="python" and code==0):#si reponse directe
                for i in range(len(listeMot)):
                    if listeMot[i].strip()=="%OUT%":
                        try:
                            resOut=resOut.decode()
                        except:
                            resOut=resOut
                        listeMot[i]=resOut.strip()
                for i in range(len(listeMot)):
                    if listeMot[i].strip()=="%IN%":
                        listeMot[i]=resIn.strip()
                rep=" ".join(listeMot)
            else:# si besoin de precision, on affiche le resultat de la fonction
                try:
                    rep=resOut.decode()
                except:
                    rep=resOut
            if action=="fichier" and code==0:
                type="F"
            else:
                type="T"
        if code==0:
            action,infos="",""
    elif action!="":
        type="T"
        if re.search("annule",phrase,re.IGNORECASE):
            infos=[]
            code=0
            action=""
        else:
            fct=infos[len(infos)-1]
            resOut,infos=eval(fct+"("+str(code)+",'"+str(phrase)+"',"+str(infos)+")")
            code=infos[1]
            if code==0:
                action=""
                infos=[]
                listRep=reponse.split("/")
                rep=choice(listRep)
                listeMot=rep.split(" ")
                for i in range(len(listeMot)):
                    if listeMot[i].strip()=="%OUT%":
                        try:
                            resOut=resOut.decode()
                        except:
                            resOut=resOut
                        listeMot[i]=resOut.strip()
                for i in range(len(listeMot)):
                    if listeMot[i].strip()=="%IN%":
                        listeMot[i]=resIn.strip()
                rep=" ".join(listeMot)
            else:
                action=""
                code=0
                infos=[]
                try:
                    resOut=resOut.decode()
                except:
                    resOut=resOut
                rep=resOut
    else:
        type="T"
        rep=reponse
    if re.search("\d{4}-\d{2}-\d{2}",rep): #reformattage des dates
        m=re.search("\d{4}-\d{2}-\d{2}",rep)
        date=m.group(0)
        d=date.split("-")
        newDate=d[2]+" "+d[1]+ " "+d[0]
        rep=re.sub("\d{4}-\d{2}-\d{2}",newDate,rep)
        rep=re.sub("T\d+:\d+","",rep)#suppression de l'heure
    reponse=Config.defaultResponse
    return type,str(rep.strip())


def run():
    while 1:
        quest=input(">")
        if quest =="quit":
            exit(0)
        t,rep=analyse(quest,"florent")
        print("==>"+rep)

#Proxy.connectProxy("https")
#run()
