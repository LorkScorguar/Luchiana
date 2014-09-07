import base64
import subprocess
import re
import builtins

def sendFichier(codeErreur=0,phrase="",infos=[]):
    rep=""
    if codeErreur==0:
        try:
            m=re.search("[A-Za-z]*.\.[A-Za-z]*",phrase)
            fileName=m.group(0)
            res,inf=searchFile(codeErreur,fileName,infos)
            if inf[1]==0:#un seul fichier
                rep=convertFileToSend(res)
                builtins.sendHandler.sendFile(rep,fileName)
                rep="Fichier envoyé"
            else:
                rep=res
            infos=inf
        except:
            rep="Je n'ai pas compris le nom du fichier"
            infos=["fichier",1,"FileManager.sendFichier"]
    else:
        res,inf=searchFile(codeErreur,phrase,infos)
        rep=convertFileToSend(res)
        builtins.sendHandler.sendFile(rep,infos[2])
        rep="Fichier envoyé"
        infos=inf
    infos[len(infos)-1]="FileManager.sendFichier"
    return rep,infos

def searchFile(codeErreur=0,fileName="",infos=[]):
    rep=""
    if codeErreur==0:
        path=""
        try:
            lpath2=[]
            r=subprocess.check_output("locate "+fileName,shell=True)
            lpath=r.decode().split("\n")
            for elem in lpath:
                if elem!="":
                    lpath2.append(elem)        
            if len(lpath2)==1:
                rep=lpath2[0]
            else:
                codeErreur=1
                rep="Plusieurs fichiers trouvés, lequel convient:\n"
                i=0
                for path in lpath2:
                    rep+=str(i)+")"+path+"\n"
                    i+=1
                path=lpath2
        except:
            rep="Aucun fichier trouvé"
            codeErreur=2
    else:
        for i in range(len(infos[3])):
            if i==int(fileName):
                rep=infos[3][i]
        codeErreur=0
        fileName=""
        path=""
    infos=["fichier",codeErreur,fileName,path,"FileManager.searchFile"]
    return rep,infos

def convertFileToSend(file):
    fichier=open(file,"rb").read()
    data=base64.b64encode(fichier)
    return data

def convertFileReceive(data,fileName):
    file=open("fichiers/"+fileName,"wb")
    data2=base64.b64decode(data)
    file.write(data2)
    return "ok"


