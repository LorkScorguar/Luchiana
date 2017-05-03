#!/usr/bin/python3
"""
Module de création du fichier de CONFIGuration
"""
import getpass
import sys
sys.path.append('server')
import Securite
import Database

CONFIG = """
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
freebase_apikey=FREEBASE_KEY
service_url="https://www.googleapis.com/freebase/v1/search"
service_url2="https://www.googleapis.com/freebase/v1/topic"
defaultFreebaseResponse="Impossible de trouver l'information"

#database
listeFichiers=["actions-fr","informatique-fr","politesse-fr","simple-fr"]

#Weather
weather_apikey=OPENWEATHER_KEY

#News
news_url=[NEWS_URL]
topics=[TOPICS]
reddit=[REDDIT]
"""

fichier = open("CONFIG.py", "w")
ip = input("Quelle est votre adresse ip?")
clef = input("Entrer la clef qui sera utiliser pour chiffrer les informations critiques: ")
email = input("Entrer le compte gmail réservé pour votre IA, ou le votre: ")
password = getpass.getpass("Entrer le mot de passe associé: ")
freebase = input("Entrer votre clef api pour freebase:")
weather = input("Entrer votre clef api pour openweathermap:")
news_url = input("Entrer les urls des fluxs rss que vous voulez suivre (séparé par des virgules): ")
topics = input("Enter la liste des sujets qui vous intéressent (séparé par des virgules): ")
reddit = input("Enter la liste des subreddit qui vous intéressent (séparé par des virgules): ")
CONFIG = CONFIG.replace("IPADDRESS", "'"+ip+"'")
CONFIG = CONFIG.replace("CLEF", "'"+clef+"'")
CONFIG = CONFIG.replace("EMAIL", "'"+email+"'")
CONFIG = CONFIG.replace("FREEBASE_KEY", "'"+freebase+"'")
CONFIG = CONFIG.replace("OPENWEATHER_KEY", "'"+weather+"'")
CONFIG = CONFIG.replace("PASSWORD", "'"+Securite.vigenere(password, clef, "1")+"'")
CONFIG = CONFIG.replace("NEWS_URL", '","'.join(news_url.split(","))+'"')
CONFIG = CONFIG.replace("TOPICS", '"'+'","'.join(topics.split(","))+'"')
CONFIG = CONFIG.replace("REDDIT", '"'+'","'.join(reddit.split(","))+'"')
fichier.write(CONFIG)
fichier.close()

Database.run()
