import socket
import readline
import atexit
import os
import getpass
import re
import Securite

clef="cipher key - to replace"
HOST, PORT = "127.0.0.1", 9998

try:
	import gtk
	import pynotify
	pynotify.init( "Luchiana" )
except:
    print("Vous n'avez pas pynotify")


histfile = ".luchiana_history"
try:
    readline.read_history_file(histfile)
    #print("history")
except IOError:
    pass
atexit.register(readline.write_history_file, histfile)

def encodeMsg(message):
	texte=unicode(Securite.vigenere(message,clef,"1"),'iso-8859-1').encode('utf-8')
	return texte

def decodeMsg(message):
    message=unicode(message,'utf-8').encode('iso-8859-1')
    texte=Securite.vigenere(message,clef,"2")
    texte=texte.decode('iso-8859-1').encode('utf-8')
    return texte

def sendMsg(type,message):
    sock.send(type+";"+encodeMsg(message))
#    print(type+";"+encodeMsg(message))
#	sock.send(encodeMsg(message))

def receiveMsg():
    rec=sock.recv(1024).strip()
#    print(rec)
    temp=rec.split(";")
    type=temp[0]
    return type,decodeMsg(temp[1])
#	return type,decodeMsg(rec)

def sendFile():
    f="test.txt"
    file=open(f,"r")
    sock.send("F;"+f+";"+file.read())

def notify(phrase):
	temp=phrase.split(";")
	title=temp[1]
	body=temp[2]
	type=temp[3]
	n = pynotify.Notification(title,body)
	if (type=="1"):
		n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_NETWORK, gtk.ICON_SIZE_LARGE_TOOLBAR))
		n.set_urgency(pynotify.URGENCY_LOW)
	elif (type=="2"):
		n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_LARGE_TOOLBAR))
		n.set_urgency(pynotify.URGENCY_LOW)
	elif (type=="3"):
		n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_APPLY, gtk.ICON_SIZE_LARGE_TOOLBAR))
		n.set_urgency(pynotify.URGENCY_LOW)
	else:
		n.set_icon_from_pixbuf(gtk.Label().render_icon(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_LARGE_TOOLBAR))
		n.set_urgency(pynotify.URGENCY_LOW)
	#n.set_timeout(2)
	n.show()

def clientQuit():
	print("A bientot")
	sock.close()
	#quit()
	os._exit(0)
	#os.kill(os.getpid(), signal.SIGINT)

def connect():
	global sock
	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
	    sock.connect((HOST, PORT))
	except ValueError:
	    print("there is an error")

