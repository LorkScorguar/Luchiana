#!/usr/bin/python3.2
#voir pour pieces jointes

import smtplib
import imaplib
import os
import sys
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import Config
import Securite
import email

def sendHtmlMail(subject,content,recipient):
    sender = Config.email
    #recipient = "lorkscorguar@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    # Create the body of the message (a plain-text and an HTML version).
    text = content
    html = content
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    s = smtplib.SMTP(Config.smtp,Config.smtpPort)
    s.ehlo()
    s.starttls()
    s.login(sender,Securite.vigenere(Config.password,Config.clef,'2'))
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(sender, recipient, msg.as_string())
    s.quit()
    return "ok"

def sendTextMail(subject,content,dest):
    fromaddr = Config.email
    smtp = smtplib.SMTP(Config.smtp,Config.smtpPort)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(Config.email,Securite.vigenere(Config.password,Config.clef,'2'))
    msg=MIMEText(content)
    #print(dest)
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = dest
    smtp.sendmail(fromaddr,dest,msg.as_string())
    smtp.close()
    return "ok"
    
def checkGmail():
    obj = imaplib.IMAP4_SSL(Config.smtp,Config.smtpPortSSL)
    obj.login(Config.email,Securite.vigenere(Config.password,Config.clef,'2'))
    obj.select()
    obj.fetch("1", "(RFC822)")
    rep=obj.search(None,'UnSeen')
    rep=str(rep[1]).replace('[','')
    rep=rep.replace(']','')
    if rep == "b''":
        nb=0
        listeMail=[]
    else:
        nb=len(rep.split(" "))
        listeMail=rep[0]
    return nb,listeMail

def readMail(id):
    exp,dest,sujet,contenu="","","",""
    mail = imaplib.IMAP4_SSL(Config.smtp,Config.smtpPortSSL)
    mail.login(Config.email,Securite.vigenere(Config.password,Config.clef,"2"))
    mail.select("inbox")
    r,d=mail.fetch(str(id),"(RFC822)")
    message=d[0][1].decode('utf-8')
    email_message=email.message_from_string(message)
    dest=email_message['To']
    exp=email_message['From']
    exp=exp[10:]
    exp=exp.replace("?= "," ")
    exp=exp.replace("=","\\x")
    exp=exp.replace("_"," ")
    exp=exp.lower()
    print(exp.encode('iso-8859-1').decode())
    return exp,dest,sujet,contenu

def addContact(codeErreur=0,phrase="",infos=[]):
    file=open("database/contacts","a")
    rep=""
    file.close()
    return "ok"

def searchContact(phrase):
    mail=""
    file=open("database/contacts","r")
    for line in file:
        temp=line.split(";")
        if re.search(temp[0],phrase):
            mail=temp[1].strip()
    file.close()
    return mail

def envoieMail(codeErreur=0,phrase="",infos=[]):
    #destinataire,sujet,contenu
    rep=""
    if len(infos)>1:
        mailD=infos[2]
        mailS=infos[3]
        mailC=infos[4]
    else:
        mailD,mailS,mailC="","",""
    if re.search("\w+@\w+\.\w{2,3}",phrase):
        m=re.search("\w+@\w+\.\w{2,3}",phrase)
        mailD=m.group(0).strip()
    if codeErreur==1:
        mailD=phrase
    elif codeErreur==2:
        mailS=phrase
    elif codeErreur==3:
        mailC=phrase
    if mailD=="":
        mailD=searchContact(phrase)
    if mailD=="":
        rep="Quel est le destinataire?"
        codeErreur=1
    elif mailS=="":
        rep="Quel est le sujet?"
        codeErreur=2
    elif mailC=="":
        rep="Quel est le contenu?"
        codeErreur=3
    else:
        sendHtmlMail(mailS,mailC,mailD)
        rep="Mail envoyé à "+mailD+" avec pour sujet "+mailS+" et comme texte: "+mailC
        codeErreur=0
        mailC=""
        mailS=""
        mailD=""
    infos=["mail",codeErreur,mailD,mailS,mailC,"Mail.envoieMail"]
    return rep,infos

"""Proxy.connectProxy('https')
infos=[]
code=0
phrase=""
while 1:
    phrase=input('>')
    if phrase=="quit":
        quit()
    rep,infos=envoieMail(code,phrase,infos)    
    print(rep)
    code=infos[1]
"""
"""n,liste=checkGmail()
print(n)
print(liste)
id=input("quel id?")
e,d,s,c=readMail(id)
print(e)
print(d)
print(s)
print(c)
"""
