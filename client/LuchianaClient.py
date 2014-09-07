#!/usr/bin/python2.7
#http://www.pygtk.org/docs/pygtk/gtk-stock-items.html
import getpass
import re
import Client
import Audio
import time
import threading
import subprocess
import os

stop=False
son=False

def connection():
    Client.connect()
    identify=0
    essai=0
    while identify==0 and essai < 3:
        pseudo=raw_input("Entrer votre pseudonyme: ")
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
            type,received = Client.receiveMsg()
            if type=="N":
                #print(received)
                Client.notify(received)
            else:
                print("-->%s" % received)
                if son:
                    adire=received[:-14]
                    Audio.parle(adire)
            time.sleep(0.01)
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
            data = raw_input(">")
            if data == "quit":
                a.stop()
                self.stop()
            elif data == "Tais toi!":
                son=False
            elif data == "Parle!":
                son=True
            elif data == "Fichier":
                Client.sendFile()
            elif data == "p":
                msg=Audio.ecoute()
                if msg != "":
                    Client.sendMsg("T",str(msg))
            elif len(data):
                Client.sendMsg("T",str(data))
            else:
                continue
            time.sleep(0.01)
    def stop(self):
        self._stopevent.set( )
        Client.clientQuit()

i=connection()
if i == 1:
	Client.notify("notif;Connection;Vous etes desormais connecte a Luchiana;1")
	#a=threading.Thread(None,listenPort,None)
	a=ListenPort('lp')
	b=ListenUser('lu')
	#b=threading.Thread(None,listenUser,None)
	a.start()
	b.start()














