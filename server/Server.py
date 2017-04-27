import socket
import threading
import socketserver
import datetime
import builtins
import hashlib
import re

import Securite
import Database
import Cerveau
import Config
import FileManager

clef=Config.clef

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def sendMsg(self,typ,message):
        t=str(message)
        d=Securite.vigenere(t,clef,"1")	
        self.request.sendall(bytes(typ+";"+d+"\n",'utf-8'))
    
    def sendFile(self,data,fileName):
        self.request.sendall(bytes("F;","utf-8")+data+bytes(";"+fileName,"utf-8"))

    def handle(self):
        logFile=open("logs","a")
        builtins.sendHandler=self
        builtins.init=1
        essai=0
        identify=0
        while essai < 3:
            rec = self.request.recv(1024).strip()
            if len(rec)>0:
                clair = Securite.vigenere(rec[2:].decode(),clef,"2")
                r = clair.split(";,;")
                password=r[1]	
                username=r[0]
                mp=Database.searchUser(username).strip()
                if mp=="invalide":
                    self.sendMsg("L","identify=0")
                    essai=essai+1
                else:					
                    if hashlib.sha224(password.encode('utf-8')).hexdigest()==mp:
                        identify=1
                        self.sendMsg("L","identify=1")
                        logFile.write(username+";"+datetime.datetime.now().isoformat()+"\n")
                        break
                    else:
                        self.sendMsg("L","identify=0")
                        essai=essai+1
                #print(identify)
            else:
                builtins.init=0
                print("client deconnecte")
                break

        while 1 and identify == 1:
            suivi=open("suivi","r")
            nbUser=0
            for ligne in suivi:
                nbUser=int(ligne.strip())
            nbUser=nbUser+1
            suivi=open("suivi","w")
            suivi.write(str(nbUser))
            suivi.close()
            d = self.request.recv(1024).strip()
            if len(d)>0:
                t=d.decode()
                temp=t.split(";")
                typ=temp[0]
                if typ == "T":
                    data = Securite.vigenere(temp[1],clef,"2")
                    cur_thread = threading.current_thread()
                    typ,answer=Cerveau.analyse(data,username)
    
                    if username =="florent":
                        answer+=" (from"+str(cur_thread.name)+")"
                    self.sendMsg(typ,answer)
                elif typ == "F":
                    complete=False
                    while not complete:
                        d += self.request.recv(1024).strip()
                        t=d.decode()
                        if re.search(";[A-Za-z]*.\.[A-Za-z]*",t):
                            complete=True
                    temp=t.split(";")
                    data=temp[1]
                    fileName=temp[2]
                    FileManager.convertFileReceive(data,fileName)
                    self.sendMsg("T","Fichier "+fileName+" bien recu")
            else:
                essai=0
                identify=0
                builtins.init=0
                print("client deconnecte")
#                Cerveau.cleanHistory()
                break

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
