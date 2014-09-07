#!/usr/bin/python3.2

import subprocess
import time
import re

def play(type):
    direction=""
    if re.search("avance",type):
        direction="lfrf"
    elif re.search("recule",type):
        direction="lbrb"
    elif re.search("gauche",type):
        direction="lbrf"
    elif re.search("droite",type):
        direction="lfrb"
    elif re.search("fire",type):
        direction="fire"
    else:
        direction="lsrs"
    file=direction+"orangetank"
    file=file+"flip.wav"
    #print("Testing "+type)
    proc=subprocess.Popen(["mplayer","database/raw/"+file],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout = proc.communicate()[0]
    time.sleep(1)

"""play("avance")
play("gauche")
play("avance")
play("recule")
play("stop")
"""
