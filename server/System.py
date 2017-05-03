"""
module contenant le necessaire de communication avec le systeme
pour recuperer des infos, ram, cpu, temp etc
"""
import os
import subprocess
import threading
import builtins
import re
import ipaddress
from uuid import getnode

def info():
    """Récupere diverses infos système"""
    uname = os.uname()
    kernel = uname[2]
    hostname = uname[1]
    architecture = uname[4]
    memUsed = subprocess.check_output("free -m | grep buffers/cache |"\
                                      " awk '{print $3}'", shell=True)
    memTotal = subprocess.check_output("free -m | grep Mem |"\
                                       " awk '{print $2}'", shell=True)
    memUsed = str(memUsed.strip(), 'utf-8')
    memTotal = str(memTotal.strip(), 'utf-8')
    infos = "kernel %s %s on %s\nMemory %sMo/%s" % (kernel, architecture,\
                                                    hostname, memUsed, memTotal)
    return infos

class Command():
    """Class de gestion de l'exécution des commandes"""
    def __init__(self, name, command):
        """init"""
        self.name = name
        self.command = command
        self.result = ""
        self.codeSortie = 256
    def getName(self):
        """Obtenir le nom de la commande"""
        return self.name
    def execute(self):
        """Exécute la commande"""
        self.process = subprocess.Popen(self.command, shell=True,\
                                        stdout=subprocess.PIPE,\
                                        stderr=subprocess.PIPE)
        self.result = self.process.communicate()[0].split(b'\n')
        self.codeSortie = self.process.returncode
        res = self.getExitCode()
        if res == 0:
            builtins.sendHandler.sendMsg("N", "notif;Commande;Commande "+\
                                              self.name+\
                                              " executee avec succes;3")
        else:
            builtins.sendHandler.sendMsg("N", "notif;Commande;La commande "+\
                                              self.name+" a rencontree une "+\
                                              "erreur lors de son execution;2")
    def getResult(self):
        """Obtenir le résultat de la commande"""
        return self.result
    def getExitCode(self):
        """Obtenir le code retour de la commande"""
        return self.codeSortie

def command(afaire):
    """Permet d'exécuter une commande"""
    nom = ""
    if re.search("^;", afaire):
        com = afaire[1:]
    else:
        com = afaire
    nom = com.split(" ")
    cmd = Command(nom[0], com)
    threadCommande = threading.Thread(None, cmd.execute, None)
    threadCommande.start()
    inf = "commande en cours"
    return inf

def getMac():
    """Récupére la mac de la machine"""
    address = getnode()
    hexa = iter(hex(address)[2:].zfill(12))
    mac = ":".join(i + next(hexa) for i in hexa)
    return mac

def ping(phrase):
    """Ping une adresse IP"""
    response = ""
    regex = re.findall(r"\b25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|"
                       r"2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|"
                       r"[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|"
                       r"[01]?[0-9][0-9]?\b",\
                     phrase)
    ip = '.'.join(regex)
    command = "ping -c 1 "
    tmp = command+ip
    sub = subprocess.Popen(tmp.split(" "), stdout=subprocess.PIPE)
    res = sub.communicate()[0].split(b"\n")
    code = sub.returncode
    if code == 0:
        response = "Ping was successful"
    else:
        response = "Ping was unsuccessful"
    infos = ["system", 0, "System.ping"]
    return response, infos

def getDiskFree():
    """Récupére l'espace disque disponible"""
    response = ""
    sub = subprocess.Popen("df", stdout=subprocess.PIPE)
    res = sub.communicate()[0].strip().decode('utf-8')
    code = sub.returncode
    tmp = res.split(" ")
    lres = list(filter(None, tmp))
    for item in lres:
        if re.search("/\n", item):
            pos = lres.index(item)
            break
    response = str(int(int(lres[pos-2])/1048576))
    infos = ["system", 0, "System.getDiskFree"]
    return response, infos

def getUptime():
    """Récupére l'uptime de la machine"""
    response = ""
    sub = subprocess.Popen("uptime", stdout=subprocess.PIPE)
    res = sub.communicate()[0].strip().decode('utf-8')
    code = sub.returncode
    response = str(res).split(" ")[2]+str(res).split(" ")[3][:-1]
    infos = ["system", 0, "System.getUptime"]
    return response, infos

def geoLoc(message):
    """Localise une IP en utilisant les infos de GeoLiteCity"""
    regex = re.findall(r"\b25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|"
                       r"2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|"
                       r"[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|"
                       r"[01]?[0-9][0-9]?\b",\
                     message)
    ip = '.'.join(regex)
    blockDb = open("database/GeoLiteCity-Blocks.csv", "r")
    locDb = open("database/GeoLiteCity-Location.csv", "r")
    integerIp = int(ipaddress.ip_address(ip))
    response = "Ip cannot be localized"
    locId = 0
    for line in blockDb:
        if not re.search("#", line):
            tmp = line.strip().replace("\"", "").split(",")
            if int(tmp[0]) <= integerIp and integerIp <= int(tmp[1]):
                locId = tmp[2]
                break
    if locId != 0:
        for line in locDb:
            if not re.search("#", line):
                tmp = line.strip().replace("\"", "").split(",")
                if tmp[0] == locId:
                    loc = tmp[3]
                    country = tmp[1]
                    #longi = tmp[6]
                    #lat = tmp[5]
                    break
        response = loc+" ("+country+")"
    infos = ["system", 0, "System.geoLoc"]
    return response, infos
