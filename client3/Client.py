"""
Module gérant l'ensemble des communications
Connexion au serveur
Encodage
Notification
"""

import socket
import atexit
import sys
import re
import os

import Securite

CLEF = "toreplace"
HOST, PORT = "127.0.0.1", 9998

try:
#    import gtk
    import notify2
    notify2.init("Luchiana")
except:
    print("Vous n'avez pas notify2")

try:
    import readline
except:
    print("No readline on Windows")


HISTFILE = os.path.dirname(__file__)+"/.luchiana_history"
try:
    readline.read_history_file(HISTFILE)
except:
    pass
try:
    atexit.register(readline.write_history_file, HISTFILE)
except:
    pass

def encodeMsg(message):
    """Permet de chiffrer un message"""
    texte = Securite.vigenere(message, CLEF, "1")
    return texte

def decodeMsg(message):
    """Permet de déchiffrer un message"""
    texte = Securite.vigenere(message, CLEF, "2")
    return texte

def sendMsg(typ, message):
    """Permet d'envoyer un message"""
    message = encodeMsg(message)
    sock.send(bytes(typ+";"+message, "utf-8"))

def sendFile(data, file_name):
    """Permet d'envoyer un fichier"""
    sock.send(bytes("F;", "utf-8")+data+bytes(";"+file_name, "utf-8"))

def receiveMsg():
    """Permet de recevoir un message"""
    rec = sock.recv(1024).strip()
    recd = rec.decode('utf-8','ignore')
    temp = recd.split(";")
    typ = temp[0]
    if typ == "F":
        complete = False
        while not complete:
            rec += sock.recv(1024).strip()
            recd = rec.decode()
            if re.search(r";[A-Za-z]*.\.[A-Za-z]*", recd):
                complete = True
        temp = recd.split(";")
        text = temp[1]
        if temp[2][-1:] == "T":
            temp[2] = temp[2][:-1]
        text += ";"+temp[2]
    else:
        text = decodeMsg(temp[1])
    return typ, text

def notify(phrase):
    """Notifie l'utilisateur"""
    res = "ok"
    temp = phrase.split(";")
    title = temp[1]
    body = temp[2]
    #type = temp[3]
    try:
        notif = notify2.Notification(title, body)
        notif.show()
    except:
        res = "ko"
        return res

def clientQuit():
    """Ferme la socket"""
    print("A bientot")
    sock.close()
    sys.exit(0)

def connect():
    """Ouvre la socket"""
    global sock
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except ValueError:
        print("there is an error")
