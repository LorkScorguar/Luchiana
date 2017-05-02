"""
module contenant le necessaire de communication avec le systeme
pour recuperer des infos, ram, cpu, temp etc
"""
import os
import subprocess
import time
import threading
import builtins
import re
import sys
import ipaddress
from uuid import getnode
import datetime

def info():
	uname=os.uname()
	kernel=uname[2]
	hostname=uname[1]
	architecture=uname[4]
	memUsed=subprocess.check_output("free -m | grep buffers/cache | awk '{print $3}'", shell=True)
	memTotal=subprocess.check_output("free -m | grep Mem | awk '{print $2}'", shell=True)
	memUsed=str(memUsed.strip(),'utf-8')
	memTotal=str(memTotal.strip(),'utf-8')
	infos="kernel %s %s on %s\nMemory %sMo/%s" % (kernel,architecture,hostname,memUsed,memTotal)
	return infos

class Command():
	def __init__(self,name,command):
		self.name=name
		self.command=command
		self.result=""
		self.codeSortie=256
	def getName(self):
		return self.name
	def execute(self):
		self.process = subprocess.Popen(self.command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		self.result = self.process.communicate()[0].split(b'\n')
		self.codeSortie = self.process.returncode
		res=self.getExitCode()
		if res==0:
			builtins.sendHandler.sendMsg("N","notif;Commande;Commande "+self.name+" executee avec succes;3")
		else:
			builtins.sendHandler.sendMsg("N","notif;Commande;La commande "+self.name+" a rencontree une erreur lors de son execution;2")
	def getResult(self):
		return self.result
	def getExitCode(self):
		return self.codeSortie

def command(afaire):
	nom=""
	if re.search("^;",afaire):
		c=afaire[1:]
	else:
		c=afaire
	nom=c.split(" ")
	cmd=Command(nom[0],c)
	threadCommande=threading.Thread(None,cmd.execute,None)
	threadCommande.start()
	inf="commande en cours"
	return inf

def receiveFile():
    return "ok"

def getMac():
	address=getnode()
	h = iter(hex(address)[2:].zfill(12))
	mac=":".join(i + next(h) for i in h)
	return mac

def ping(phrase):
	response=""
	r=re.findall(r'\b25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\b',phrase)
	ip='.'.join(r)
	command="ping -c 1 "
	tmp=command+ip
	s=subprocess.Popen(tmp.split(" "),stdout=subprocess.PIPE)
	res=s.communicate()[0].split(b"\n")
	code=s.returncode
	if code==0:
		response="Ping was successful"
	else:
		response="Ping was unsuccessful"
	infos=["system",0,"System.ping"]
	return response,infos

def getDiskFree():
	response=""
	s=subprocess.Popen("df",stdout=subprocess.PIPE)
	res=s.communicate()[0].strip().decode('utf-8')
	code=s.returncode
	tmp=res.split(" ")
	lres=list(filter(None, tmp))
	for item in lres:
		if re.search("/\n",item):
			pos=lres.index(item)
			break
	response=str(int(int(lres[pos-2])/1048576))
	infos=["system",0,"System.getDiskFree"]
	return response,infos

def getUptime():
	response=""
	s=subprocess.Popen("uptime",stdout=subprocess.PIPE)
	res=s.communicate()[0].strip().decode('utf-8')
	code=s.returncode
	response=str(res).split(" ")[2]+str(res).split(" ")[3][:-1]
	infos=["system",0,"System.getUptime"]
	return response,infos

def geoLoc(message):
    r=re.findall(r'\b25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\b',message)
    ip='.'.join(r)
    blockDb=open("database/GeoLiteCity-Blocks.csv","r")
    locDb=open("database/GeoLiteCity-Location.csv","r")
    integerIp=int(ipaddress.ip_address(ip))
    location=""
    response="Ip cannot be localized"
    locId=0
    for line in blockDb:
        if not re.search("#",line):
            tmp=line.strip().replace("\"","").split(",")
            if int(tmp[0])<=integerIp and integerIp <= int(tmp[1]):
                locId=tmp[2]
                break
    if locId!=0:
        for line in locDb:
            if not re.search("#",line):
                tmp=line.strip().replace("\"","").split(",")
                if tmp[0]==locId:
                    loc=tmp[3]
                    country=tmp[1]
                    long=tmp[6]
                    lat=tmp[5]
                    break
        response=loc+" ("+country+")"
    infos=["system",0,"System.geoLoc"]
    return response,infos
