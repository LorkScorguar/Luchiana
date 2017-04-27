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
print(d)
"""
