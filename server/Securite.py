"""
module contenant les fonction de securite
chiffrement, dechiffrement, decryptage etc
"""
import time
import re

def vigenere(phrase,clef,operation):
    #1=chiffre 2=dechiffre
    sortie, i = "", 0
    for caract in phrase:   #parcours de la chaine a traiter
        if operation == "1":    #chiffrement
            sortie = sortie + chr((ord(caract) + ord(clef[i])) % 256)
            i = i + 1   #parcours de la cle
            if i > len(clef) - 1:
                i = 0   #fin de cle atteinte, on repart au debut
        elif operation == "2":  #dechiffrement
            sortie = sortie + chr((ord(caract) - ord(clef[i])) % 256)
            i = i + 1
            if i > len(clef) - 1:
                i = 0
    return sortie

"""clef=input("entrer la clef:")
texte=input("entrer le texte:")
c=vigenere(texte,clef,"1")
print(c)
d=vigenere(c,clef,"2")
print(d)"""


def cherche_anagramme(mot):
    global dico
    res=[]
    lettres = dict((l, mot.count(l)) for l in set(mot))
    if len(mot) == 1:
        res.append(mot)
    else:
        for ana in dico:
            if len(ana)==len(mot):
                anag=True
                for lettre in mot:
                    if lettre not in ana:
                        anag=False
                if anag==True:
                    lettres2 = dict((l, ana.count(l)) for l in set(ana))
                    if lettres==lettres2:
                        res.append(ana)

    return res

def init():
    global dico
    dico=[]
    dic=open("dico/dico-fr.txt","r")
    for line in dic:
        dico.append(line.strip())

"""start=time.time()
print("init en cours")
init()
print("init en "+str(time.time()-start)+"sec")
while 1:
    mot=input("Entrer le mot à anagrammer:")
    start=time.time()
    a=cherche_anagramme(mot)
    print("Résultat en :"+str(a)+"\n"+str(time.time()-start)+"sec")
"""
