#!/usr/bin/python3
"""
Module pour piloter un Tankbot en utilisant l'emetteur fournit
"""
import subprocess
import time
import re

def play(typ):
    """fonction pour lire le bon ficheir son selon l'action demandée"""
    direction = ""
    if re.search("avance", typ):
        direction = "lfrf"
    elif re.search("recule", typ):
        direction = "lbrb"
    elif re.search("gauche", typ):
        direction = "lbrf"
    elif re.search("droite", typ):
        direction = "lfrb"
    elif re.search("fire", typ):
        direction = "fire"
    else:
        direction = "lsrs"
    file = direction+"orangetank"
    file = file+"flip.wav"
    #print("Testing "+type)
    proc = subprocess.Popen(["mplayer", "database/raw/"+file],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = proc.communicate()[0]
    time.sleep(1)

#play("avance")
#play("gauche")
#play("avance")
#play("recule")
#play("stop")
