#!/usr/bin/python3.3
"""Module Principal"""
import getpass
import re
import threading

import Client
#import Audio
#import GoogleSpeechToText as GSTT
import FileManager

SON = False


def connection():
    """Gére la connection au serveur"""
    Client.connect()
    identify = 0
    essai = 0
    while identify == 0 and essai < 3:
        pseudo = input("Entrer votre pseudonyme: ")
        password = getpass.getpass("Entrer le mot de passe: ")
        Client.sendMsg("L", pseudo+";,;"+password)
        rep = Client.receiveMsg()
        if rep[1][9:] == "1":
            identify = 1
            break
        else:
            if essai < 2:
                print("Vous avez fais une erreur\nVeuillez recommencer")
            if essai == 2:
                print("Trop d'erreurs, au revoir")
                quit()
            essai = essai+1
    return identify


class ListenPort(threading.Thread):
    """Classe pour l'écoute du port et retour à l'utilisateur"""
    def __init__(self, nom=''):
        """init"""
        threading.Thread.__init__(self)
        self.nom = nom
        self._stopevent = threading.Event()
    def run(self):
        """main"""
        global SON
        while not self._stopevent.isSet():
            typ, received = Client.receiveMsg()
            if typ == "N":
                rec = Client.notify(received)
                if rec == "ko":
                    print("\n-->%s" % received)
            elif typ == "F":
                rec = received.split(";")
                FileManager.convertFileReceive(rec[0], rec[1])
                rec = Client.notify("notif;Transfert;Fichier "+rec[1]+" bien reçu;4")
                if rec == "ko":
                    print("\n-->Fichier "+rec[1]+" bien reçu")
            else:
                print("\n-->%s" % received)
                #if SON:
                    #adire = received[:-14]
                    #Audio.parle(adire)
    def stop(self):
        """stop le thread"""
        self._stopevent.set()

class ListenUser(threading.Thread):
    """Classe pour l'écoute de l'utilisateur et envoie au serveur"""
    def __init__(self, nom=''):
        """init"""
        threading.Thread.__init__(self)
        self.nom = nom
        self._stopevent = threading.Event()
    def run(self):
        """Main"""
        global SON
        global TLP
        while not self._stopevent.isSet():
            data = input(">")
            if data == "quit":
                TLP.stop()
                self.stop()
            elif data == "Tais toi!":
                SON = False
            elif data == "Parle!":
                SON = True
            elif re.search("je.*envoie.*fichier", data):
                regex = re.search(r"[A-Za-z]*.\.[A-Za-z]*", data)
                fileName = regex.group(0)
                data2, infos = FileManager.sendFichier(0, fileName)
                if infos[1] == 0:
                    Client.sendFile(data2, fileName)
                else:
                    choix = input(data2)
                    data2, infos = FileManager.sendFichier(1, choix, infos)
            elif len(data):
                Client.sendMsg("T", str(data))
            else:
                continue
    def stop(self):
        """Ferme la connection"""
        self._stopevent.set()
        Client.clientQuit()


CONNECT = connection()
#import Proxy
#Proxy.connectProxy('https')
if CONNECT == 1:
    RES = Client.notify("notif;Connection;Vous etes desormais"
                        "connecte a Luchiana;1")
    if RES == "ko":
        print("\n-->Vous etes desormais connecte a Luchiana")
    TLP = ListenPort('lp')
    TLU = ListenUser('lu')
    #tlfs=threading.Thread(None, GSTT.listen_for_speech, None)
    TLP.start()
    TLU.start()
#   tlfs.start()
