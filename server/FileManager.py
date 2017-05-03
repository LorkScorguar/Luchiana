"""
Module de gestion d'envoie/réception de fichiers
"""
import base64
import subprocess
import re

def sendFichier(code_erreur=0, phrase="", infos=[]):
    """Fonction utiliser pour envoyer un fichier après l'avoir convertit en base64"""
    rep = ""
    try:
        regex = re.search(r"[A-Za-z]*.\.[A-Za-z]*", phrase)
        file_name = regex.group(0)
        res, inf = searchFile(code_erreur, file_name, infos)
        if inf[1] == 0:#un seul fichier
            rep = convertFileToSend(res)
        else:
            rep = res
        infos = inf
    except:
        rep = "Je n'ai pas compris le nom du fichier"
    return rep, infos

def searchFile(code_erreur=0, file_name="", infos=[]):
    """Fonction pour chercher un fichier sur le système"""
    rep = ""
    if code_erreur == 0:
        path = ""
        try:
            lpath2 = []
            res = subprocess.check_output("locate "+file_name, shell=True)
            lpath = res.decode().split("\n")
            for elem in lpath:
                if elem != "":
                    lpath2.append(elem)
            if len(lpath2) == 1:
                rep = lpath2[0]
            else:
                code_erreur = 1
                rep = "Plusieurs fichiers trouvés, lequel convient:"
                i = 0
                for path in lpath2:
                    rep += "\n "+i+")"+path
                    i += 1
                path = lpath2
        except:
            rep = "Aucun fichier trouvé"
            code_erreur = 2
    else:
        i = 0
        for i in range(len(infos[3])):
            if i == file_name:
                rep = infos[3][i]
        code_erreur = 0
        file_name = ""
        path = ""
    infos = ["fichier", code_erreur, file_name, path, "FileManager.searchFile"]
    return rep, infos

def convertFileToSend(file):
    """Convert a file to base64 string"""
    fichier = open(file, "rb").read()
    data = base64.b64encode(fichier)
    return data

def convertFileReceive(data, file_name):
    """Convertit une string base64 en fichier"""
    file = open("fichiers/"+file_name, "wb")
    data2 = base64.b64decode(data)
    file.write(data2)
    return "ok"
