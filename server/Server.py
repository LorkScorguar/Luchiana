"""
Module de gestion de la communication avec le client
Les messages ont la forme suivante:
- type;message
Le type peut être:
- L: pour le login
- T: pour du texte simple
- F: pour un fichier
- N: pour une notification
"""
import threading
import socketserver
import datetime
import builtins
import hashlib
import os
import re

import Securite
import Database
import Cerveau
import Config
import FileManager

CLEF = Config.clef

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """Classe de gestion de la communication"""
    def sendMsg(self, typ, message):
        """Fonction d'envoie de message"""
        text = str(message)
        dec = Securite.vigenere(text, CLEF, "1")
        self.request.sendall(bytes(typ+";"+dec+"\n", 'utf-8'))

    def sendFile(self, data, fileName):
        """Fonction d'envoie de fichier"""
        self.request.sendall(bytes("F;", "utf-8")+data+bytes(";"+fileName, "utf-8"))

    def handle(self):
        """Fonction principale"""
        logFile = open(os.path.dirname(__file__)+"/logs", "a")
        builtins.sendHandler = self
        builtins.init = 1
        essai = 0
        identify = 0
        while essai < 3:
            rec = self.request.recv(1024).strip()
            if len(rec) > 0:
                res = Securite.vigenere(rec[2:].decode(), CLEF, "2").split(";,;")
                password = res[1]
                username = res[0]
                mp = Database.searchUser(username).strip()
                if mp == "invalide":
                    self.sendMsg("L", "identify=0")
                    essai = essai+1
                else:
                    if hashlib.sha224(password.encode('utf-8')).hexdigest() == mp:
                        identify = 1
                        self.sendMsg("L", "identify=1")
                        logFile.write(username+";"+datetime.datetime.now().isoformat()+"\n")
                        break
                    else:
                        self.sendMsg("L", "identify=0")
                        essai = essai+1
            else:
                builtins.init = 0
                print("client deconnecte")
                break

        while 1 and identify == 1:
            suivi = open(os.path.dirname(__file__)+"/suivi", "r")
            nbUser = 0
            for ligne in suivi:
                nbUser = int(ligne.strip())
            nbUser = nbUser+1
            suivi = open(os.path.dirname(__file__)+"/suivi", "w")
            suivi.write(str(nbUser))
            suivi.close()
            dat = self.request.recv(1024).strip()
            if len(dat) > 0:
                text = dat.decode()
                temp = text.split(";")
                typ = temp[0]
                if typ == "T":
                    data = Securite.vigenere(temp[1], CLEF, "2")
                    cur_thread = threading.current_thread()
                    typ, answer = Cerveau.analyse(data, username)

                    if username == "lork":
                        answer += " (from"+str(cur_thread.name)+")"
                    self.sendMsg(typ, answer)
                elif typ == "F":
                    complete = False
                    while not complete:
                        dat += self.request.recv(1024).strip()
                        text = dat.decode()
                        if re.search(r";[A-Za-z]*.\.[A-Za-z]*", text):
                            complete = True
                    temp = text.split(";")
                    data = temp[1]
                    fileName = temp[2]
                    FileManager.convertFileReceive(data, fileName)
                    self.sendMsg("T", "Fichier "+fileName+" bien recu")
            else:
                essai = 0
                identify = 0
                builtins.init = 0
                print("client deconnecte")
#                Cerveau.cleanHistory()
                break

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Simple override"""
    pass
