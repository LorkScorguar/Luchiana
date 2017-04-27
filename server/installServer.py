#!/usr/bin/python3
config="""
#LuchianaServer
port=9998
address=IPADDRESS

#Server
clef=CLEF

#Cerveau
defaultResponse="Je ne sais pas/Je n'ai pas compris"

#Mail
email=EMAIL
password=PASSWORD
smtp="smtp.gmail.com"
smtpPort="587"
smtpPortSSL="993"

#Freebase
api_key="AIzaSyA-WMfgx3SUL4RAWRKiStbU8JV2al0DPQ0"
service_url="https://www.googleapis.com/freebase/v1/search"
defautFreebaseResponse="Impossible de trouver l'information"
"""

import getpass
import sys
sys.path.append('server')
import Securite

fichier=open("Config.py","w")
ip=input("Quelle est votre adresse ip?")
clef=input("Entrer la clef qui sera utiliser pour chiffrer les informations critiques: ")
email=input("Entrer le compte gmail réservé pour votre IA, ou le votre: ")
password=getpass.getpass("Entrer le mot de passe associé: ")
config=config.replace("IPADDRESS","'"+ip+"'")
config=config.replace("CLEF","'"+clef+"'")
config=config.replace("EMAIL","'"+email+"'")
config=config.replace("PASSWORD","'"+Securite.vigenere(password,clef,"1")+"'")
fichier.write(config)

import Database
Database.run()
