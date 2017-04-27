import socket
import readline
import atexit
import os
import getpass
import re
import Securite

clef="toreplace"
HOST, PORT = "127.0.0.1", 9998

try:
#	import gtk
	import notify2
	notify2.init( "Luchiana" )
except:
    print("Vous n'avez pas notify2")


histfile = ".luchiana_history"
try:
    readline.read_history_file(histfile)
    #print("history")
except IOError:
    pass
atexit.register(readline.write_history_file, histfile)

def encodeMsg(message):
    texte=Securite.vigenere(message,clef,"1")
    return texte

def decodeMsg(message):
    texte=Securite.vigenere(message,clef,"2")
    return texte

def sendMsg(typ,message):
    message=encodeMsg(message)
    sock.send(bytes(typ+";"+message,"utf-8"))

def sendFile(data,fileName):
    sock.send(bytes("F;","utf-8")+data+bytes(";"+fileName,"utf-8"))

def receiveMsg():
    rec=sock.recv(1024).strip()
    t=rec.decode()
    temp=t.split(";")
    typ=temp[0]
    if typ=="F":
        complete=False
        while not complete:
            rec += sock.recv(1024).strip()
            t=rec.decode()
            if re.search(";[A-Za-z]*.\.[A-Za-z]*",t):
                complete=True
        temp=t.split(";")
        text=temp[1]
        if temp[2][-1:]=="T":
            temp[2]=temp[2][:-1]
        text+=";"+temp[2]
    else:
        text=decodeMsg(temp[1])
    return typ,text

def notify(phrase):
        res="ok"
	temp=phrase.split(";")
	title=temp[1]
	body=temp[2]
	type=temp[3]
        try:
	    n = notify2.Notification(title,body)
	    n.show()
        except:
            res="ko"
        return res

def clientQuit():
	print("A bientot")
	sock.close()
	os._exit(0)

def connect():
	global sock
	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
	    sock.connect((HOST, PORT))
	except ValueError:
	    print("there is an error")

