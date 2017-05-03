"""
Module de fonction mathématiques
"""
import re
import math

def pythagore(texte):
    """utilisation: pythagore("l1;l2") ou pythagore("l1;l2;l3")"""
    res = "pythagore"
    #l1 et l2, on cherche l3
    if re.search(r"^[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?"\
                 r"((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?$", texte):
        temp = texte.split(";")
        res = "Le 3eme côté mesure "+\
              str(math.sqrt(math.pow(float(temp[0]), 2)+math.pow(float(temp[1]), 2)))
    #l1, l2 et l3 on cherche si trg rectangle
    elif re.search(r"^[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?"\
                   r"((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?"\
                   r"((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?$", texte):
        temp = texte.split(";")
        if math.pow(float(temp[0]), 2)+\
            math.pow(float(temp[1]), 2) == math.pow(float(temp[2]), 2):
            res = "Selon Pythagore, ce triangle est rectangle."
        else:
            res = "Selon Pythagore, ce triangle n'est pas rectangle."
    return res

def thales(texte):
    """utilisation: thales("l1;l2;l3") ou thales("l1;l2;l3;l4")"""
    res = "thales"
    if re.search(r"^[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?"\
                 r"((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?((\d+(\.\d*)?)|"\
                 r"\.\d+)([eE][+-]?[0-9]+)?$", texte):
        temp = texte.split(";")
        res = "Le 4eme côté mesure "+str((float(temp[2])*float(temp[1]))/float(temp[0]))
    elif re.search(r"^[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?"\
                   r"((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?((\d+(\.\d*)?)|"\
                   r"\.\d+)([eE][+-]?[0-9]+)?;[+-]?((\d+(\.\d*)?)|"\
                   r"\.\d+)([eE][+-]?[0-9]+)?$", texte):
        temp = texte.split(";")
        if float(temp[0])/float(temp[1]) == float(temp[2])/float(temp[3]):
            res = "Les droits sont parallèles"
        else:
            res = "Les droites ne sont pas parallèles"
    return res


def perimetre(texte):
    """utilisation: perimetre("type l;l2")"""
    res = "Le périmétre est "
    tmp = texte.split(" ")
    typ = tmp[0]
    lon = tmp[1]
    if typ == "cercle":
        res += str(float(lon)*math.pi)
    elif typ == "rectangle":
        temp = lon.split(";")
        res += str((float(temp[0])+float(temp[1]))*2)
    elif typ == "carre" or typ == "losange":
        res += str(float(lon)*4)
    elif typ == "triangle":
        temp = lon.split(";")
        res += str(float(temp[0])+float(temp[1])+float(temp[2]))
    else:
        res = "erreur, type inconnu"
    return str(res)


def surface(texte):
    """utilisation: surface("type l;l2")"""
    res = "La surface est "
    tmp = texte.split(" ")
    typ = tmp[0]
    lon = tmp[1]
    if typ == "cercle":
        res += str(math.pow(float(lon), 2)*math.pi)
    elif typ == "rectangle":
        temp = lon.split(";")
        res += str(float(temp[0])*float(temp[1]))
    elif typ == "carre":
        temp = lon.split(";")
        res += str(float(temp[0])*float(temp[0]))
    elif typ == "cylindre":
        temp = lon.split(";")
        res += str(math.pi*float(temp[0])*float(temp[1]))
    elif typ == "losange" or typ == "triangle":
        temp = lon.split(";")
        res += str(float(temp[0])*float(temp[1])/2)
    else:
        res = "erreur, type inconnu"
    return str(res)

def volume(texte):
    """utilisation: volume("type l;l2")"""
    res = "Le volume est "
    tmp = texte.split(" ")
    typ = tmp[0]
    lon = tmp[1]
    if typ == "sphere":
        res += str(float(4/3)*math.pi*math.pow(float(lon), 3))#4/3*pi*r^3
    elif typ == "parallelepipede":
        temp = lon.split(";")
        res += str(float(temp[0])*float(temp[1])*float(temp[2]))#a*b*c
    elif typ == "cube":
        temp = lon.split(";")
        res += str(float(temp[0])*float(temp[0])*float(temp[0]))#a*b*c
    elif typ == "cylindre":
        temp = lon.split(";")
        res += str(math.pi*math.pow(float(temp[0]), 2)*float(temp[1]))#pi*R²*h
    else:
        res = "erreur, type inconnu"
    return str(res)

def calcul(texte):
    """utilisation: calcul(calcul)"""
    temp = texte.split(" ")
    for i in range(len(temp)-1):
        if temp[i] == "racine":
            temp[i] = "math.sqrt("+temp[i+1]+")"
            del temp[i+1]
        if temp[i] == "cosinus":
            temp[i] = "math.cos("+temp[i+1]+")"
            del temp[i+1]
        if temp[i] == "sinus":
            temp[i] = "math.sin("+temp[i+1]+")"
            del temp[i+1]
        if temp[i] == "tangente":
            temp[i] = "math.tan("+temp[i+1]+")"
            del temp[i+1]
    for i in range(len(temp)):
        if re.search("pi", temp[i]):
            temp[i] = temp[i].replace("pi", str(math.pi))
    for i in range(len(temp)):
        if re.search("puissance", temp[i]):
            temp[i] = temp[i].replace("puissance", "**")
    equation = " ".join(temp)
    try:
        res = eval(equation)
    except:
        res = resolution1(equation)
    return str(res)


def resolution1(texte):
    """utilisation: resolution1(equation)"""
    res = "x="
    i = re.search(r"[+-/*]?(\d+(\.\d*)?)+x", texte)
    j = re.search(r"([+-/*](\d+(\.\d*)?)+=)|([+-/*](\d+(\.\d*)?)+$)", texte)
    k = re.search(r"(=[+-/*]?(\d+(\.\d*)?)+$)|([+-/*]?(\d+(\.\d*)?)+=)", texte)
    try:
        a = i.group(0)[:-1]
    except:
        a = ""
    try:
        b = j.group(0)
        if b[-1:] == "=":
            b = b[:-1]
    except:
        b = ""
    try:
        y = k.group(0)
        if y[:1] == "=":
            y = y[1:]
        elif y[-1:] == "=":
            y = y[:-1]
    except:
        y = ""
    #print("a="+a+" b="+b+" y="+y)
    if a and b and y:
        if b[:1] == "+":
            t = "("+y+"-"+b+")/"+a
        else:
            t = "("+y+"+"+b+")/"+a
    elif a and y:
        t = y+"/"+a
    elif b and y:
        if b[:1] == "+":
            t = y+"-"+b
        else:
            t = y+"+"+b
    elif y:
        t = y
    else:
        t = ""
    res = eval(t)
    return str(res)

def run(texte):
    """Fonction de test"""
    res = ""
    if texte == "quit":
        quit()
    if re.search("pythagore", texte):
        regex = re.search(r"[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?"\
                          r"(;[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?){1,2}",\
                          texte)
        res = pythagore(regex.group(0))
    elif re.search("thales", texte):
        regex = re.search(r"[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?(;[+-]?"\
                          r"((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?){2,3}", texte)
        res = thales(regex.group(0))
    elif re.search("perimetre", texte):
        try:
            regex = re.search("carre|rectangle|cercle|losange|triangle", texte)
            text = regex.group(0)
            regex2 = re.search(r"(\d+)(;\d+)?", texte)
            text += " "+regex2.group(0)
            #print(text)
        except:
            text = "inconnu"
        res = perimetre(text)
    elif re.search("surface", texte):
        try:
            regex = re.search("carre|cercle|rectangle|cylindre|losange|triangle", texte)
            text = regex.group(0)
            regex2 = re.search(r"(\d+)(;\d+)?", texte)
            text += " "+regex2.group(0)
            #print(text)
        except:
            text = "inconnu"
        res = surface(text)
    elif re.search("volume", texte):
        try:
            regex = re.search("sphere|parallelepipede|cube|cylindre", texte)
            text = regex.group(0)
            regex2 = re.search(r"(\d+)(;\d+)?", texte)
            text += " "+regex2.group(0)
            #print(text)
        except:
            text = "inconnu"
        res = volume(texte)
    else:
        try:
            res = calcul(texte)
        except:
            res = "impossible"
    #print(str(res))
    return res

#texte=input("entrer du texte")
#res=run(texte)
#print(res)
