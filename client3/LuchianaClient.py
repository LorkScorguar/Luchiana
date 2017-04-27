#!/usr/bin/python3.3
#http://www.pygtk.org/docs/pygtk/gtk-stock-items.html
import getpass
import re
import time
import threading
import subprocess
import os

import Client
#import Audio
#import GoogleSpeechToText as GSTT
import FileManager

stop=False
son=False


def connection():
    Client.connect()
    identify=0
    essai=0
    while identify==0 and essai < 3:
        pseudo=input("Entrer votre pseudonyme: ")
        password=getpass.getpass("Entrer le mot de passe: ")
        Client.sendMsg("L",pseudo+";,;"+password)
        rep=Client.receiveMsg()
        if(rep[1][9:]=="1"):
            identify=1
            break
        else:
            if(essai<2):
                print("Vous avez fais une erreur\nVeuillez recommencer")
            if(essai==2):
                print("Trop d'erreurs, au revoir")
                quit()
            essai=essai+1
    return identify


class ListenPort(threading.Thread):
    def __init__(self, nom = ''):
        threading.Thread.__init__(self)
        self.nom = nom
        self._stopevent = threading.Event( )
    def run(self):
        global son
        while not self._stopevent.isSet():
            typ,received = Client.receiveMsg()
            if typ=="N":
                r=Client.notify(received)
                if r=="ko":
                    print("\n-->%s" % received)
            elif typ=="F":
                r=received.split(";")
                FileManager.convertFileReceive(r[0],r[1])
                r=Client.notify("notif;Transfert;Fichier "+r[1]+" bien reçu;4")
                if r=="ko":
                    print("\n-->Fichier "+r[1]+" bien reçu")
            else:
                print("\n-->%s" % received)
                if son:
                    adire=received[:-14]
                    #Audio.parle(adire)
    def stop(self):
        self._stopevent.set( )

class ListenUser(threading.Thread):
    def __init__(self, nom = ''):
        threading.Thread.__init__(self)
        self.nom = nom
        self._stopevent = threading.Event( )
    def run(self):
        global son
        global a
        while not self._stopevent.isSet():
            data = input(">")
            if data == "quit":
                a.stop()
                self.stop()
            elif data == "Tais toi!":
                son=False
            elif data == "Parle!":
                son=True
            elif re.search("je.*envoie.*fichier",data):
                m=re.search("[A-Za-z]*.\.[A-Za-z]*",data)
                fileName=m.group(0)
                data2,infos=FileManager.sendFichier(0,fileName)
                if infos[1]==0:
                    Client.sendFile(data2,fileName)
                else:
                    choix=input(data2)
                    data2,infos=FileManager.sendFichier(1,choix,infos)
            elif len(data):
                Client.sendMsg("T",str(data))
            else:
                continue
    def stop(self):
        self._stopevent.set( )
        Client.clientQuit()


i=connection()
#import Proxy
#Proxy.connectProxy('https')
if i == 1:
    r=Client.notify("notif;Connection;Vous etes desormais connecte a Luchiana;1")
    if r=="ko":
        print("\n-->Vous etes desormais connecte a Luchiana")
    a=ListenPort('lp')
    b=ListenUser('lu')
    #c=threading.Thread(None, GSTT.listen_for_speech, None)
    a.start()
    b.start()
#    c.start()
