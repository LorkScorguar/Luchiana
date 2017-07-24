"""
Module de reflexion
Permet de trouver la réponse la plus appropriée pour chaque question
"""
#Modules de base
import re
import datetime
import subprocess
from random import choice

#Modules specifiques
import Proxy
import Freebase
import System
import Web
import Math
import Mail
import Config
import FileManager

reponse = Config.defaultResponse
listeFichiers = Config.listeFichiers
INFOS = []
CODE = 0
ACTION = ""


Articles = ["le", "la", "les", "l", "un", "une", "des", "du"]
PronomsSujet = ["j", "je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"]
PronomsPossessif = ["mon", "ton", "son", "ma", "ta", "sa", "mes", "tes", "ses"]
Question = ["comment", "quel", "quelle", "quand", "combien", "qui", "que",\
            "qu'est-ce", "qu'est ce"]
Ponctuation = [".", "!", "?", "...", ",", ";", ":", "(", ")"]


def analyse(phrase, username):
    """fonction d'analyse de l'entrée utilisateur"""
    global ACTION
    global CODE
    global INFOS
    global reponse
    typ = ""
    resIn, resOut = "", ""
    act, typeAct, rep = "", "", ""
    if re.search("[A-Z].*", phrase):
        regex = re.search("[A-Z].*", phrase)
        resIn = regex.group(0)
    if ACTION == "":#gestion passage initial
        if re.search(r"(calcul|combien|pythagore|thales|perimetre|surface|"\
                     r"volume|triangle){1, }[-+*\/]?\d+", phrase,\
                     re.IGNORECASE) or re.search(r"([-+*\/]+\d+)+", phrase):
            typ = "T"
            rep = Math.run(phrase)
        else:
            possible = 0
            for fich in listeFichiers:
                fichier = open(os.path.dirname(__file__)+"/database/"+fich, "r")
                for ligne in fichier:
                    temp = ligne.split(";")
                    mots = temp[0]
                    i = 0
                    while i < len(mots):
                        if re.search(mots, phrase, re.IGNORECASE):
                            t = mots.split(".*")
                            if len(t) > possible:
                                possible = len(t)
                                typeAct = temp[1]
                                act = temp[2]
                                reponse = temp[3]
                        i += 2
            typ = "T"
            listRep = reponse.split("/")
            rep = choice(listRep)

            #remplacement du %IN% dans l'action
            listeAct = act.split(" ")
            for i in range(len(listeAct)):
                if listeAct[i].strip() == "%IN%":
                    listeAct[i] = "'"+phrase.strip()+"'"
            act = " ".join(listeAct)
            if typeAct == "bash":#récupération des infos en plus
                if re.search("%OUT%", reponse):
                    resOut = subprocess.check_output(act, shell=True)
                else:
                    resOut = System.command(act)
            elif typeAct == "python":
                resOut, INFOS = eval(act)
                ACTION = INFOS[0]
                CODE = INFOS[1]
            try:
                resOut = resOut.decode()
            except:
                resOut = resOut
            rep = rep.replace("%IN%",resIn.strip())
            rep = rep.replace("%OUT%",resOut.strip())
            if ACTION == "fichier" and CODE == 0:
                typ = "F"
            else:
                typ = "T"
        if CODE == 0:
            ACTION, INFOS = "", ""
    elif ACTION != "":
        typ = "T"
        if re.search("annule", phrase, re.IGNORECASE):
            INFOS = []
            CODE = 0
            ACTION = ""
        else:
            fct = INFOS[len(INFOS)-1]
            resOut, INFOS = eval(fct+"("+str(CODE)+", '"+str(phrase)+\
                                 "', "+str(INFOS)+")")
            CODE = INFOS[1]
            if CODE == 0:
                ACTION = ""
                INFOS = []
                listRep = reponse.split("/")
                rep = choice(listRep)
                """listeMot = rep.split(" ")
                for i in range(len(listeMot)):
                    if listeMot[i].strip() == "%OUT%":
                        try:
                            resOut = resOut.decode()
                        except:
                            resOut = resOut
                        listeMot[i] = resOut.strip()
                for i in range(len(listeMot)):
                    if listeMot[i].strip() == "%IN%":
                        listeMot[i] = resIn.strip()
                rep = " ".join(listeMot)"""
                try:
                    resOut = resOut.decode()
                except:
                    resOut = resOut
                rep = rep.replace("%IN%",resIn.strip())
                rep = rep.replace("%OUT%",resOut.strip())
            else:
                ACTION = ""
                CODE = 0
                INFOS = []
                try:
                    resOut = resOut.decode()
                except:
                    resOut = resOut
                rep = resOut
    else:
        typ = "T"
        rep = reponse
    if re.search(r"\d{4}-\d{2}-\d{2}", rep): #reformattage des dates
        regex = re.search(r"\d{4}-\d{2}-\d{2}", rep)
        date = regex.group(0)
        dat = date.split("-")
        newDate = dat[2]+" "+dat[1]+ " "+dat[0]
        rep = re.sub(r"\d{4}-\d{2}-\d{2}", newDate, rep)
        rep = re.sub(r"T\d+:\d+", "", rep)#suppression de l'heure
    reponse = Config.defaultResponse
    return typ, str(rep.strip())


def run():
    """Fonction de test"""
    while 1:
        quest = input(">")
        if quest == "quit":
            exit(0)
        _, rep = analyse(quest, "florent")
        print("==>"+rep)

#Proxy.connectProxy("https")
#run()
