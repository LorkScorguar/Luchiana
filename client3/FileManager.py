import base64
import subprocess
import re

def sendFichier(codeErreur=0,phrase="",infos=[]):
    rep=""
    try:
        m=re.search("[A-Za-z]*.\.[A-Za-z]*",phrase)
        fileName=m.group(0)
        res,inf=searchFile(codeErreur,fileName,infos)
        if inf[1]==0:#un seul fichier
            rep=convertFileToSend(res)
        else:
            rep=res
        infos=inf
    except:
        rep="Je n'ai pas compris le nom du fichier"
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
                rep="Plusieurs fichiers trouvés, lequel convient:"
                i=0
                for path in lpath2:
                    rep+="\n "+i+")"+path
                    i+=1
                path=lpath2
        except:
            rep="Aucun fichier trouvé"
            codeErreur=2
    else:
        i=0
        for i in range(len(infos[3])):
            if i==fileName:
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


