import re
import math

#utilisation: pythagore("l1;l2") ou pythagore("l1;l2;l3") 
def pythagore(texte):
        res="pythagore"
        if re.search("^[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?$",texte):#l1 et l2, on cherche l3
                temp=texte.split(";")
                res="Le 3eme côté mesure "+str(math.sqrt(math.pow(float(temp[0]),2)+math.pow(float(temp[1]),2)))
        elif re.search("^[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?$",texte):#l1, l2 et l3 on cherche si trg rectangle
                temp=texte.split(";")
                if math.pow(float(temp[0]),2)+math.pow(float(temp[1]),2)==math.pow(float(temp[2]),2):
                    res="Selon Pythagore, ce triangle est rectangle."
                else:
                    res="Selon Pythagore, ce triangle n'est pas rectangle."
        return res

#utilisation: thales("l1;l2;l3") ou thales("l1;l2;l3;l4")
def thales(texte):
    res="thales"
    if re.search("^[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?$",texte):
        temp=texte.split(";")
        res="Le 4eme côté mesure "+str((float(temp[2])*float(temp[1]))/float(temp[0]))
    elif re.search("^[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?;[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?$",texte):
        temp=texte.split(";")
        if float(temp[0])/float(temp[1]) == float(temp[2])/float(temp[3]):
            res="Les droits sont parallèles"
        else:
            res="Les droites ne sont pas parallèles"
    return res


#utilisation: perimetre("type l")
def perimetre(texte):
    res="Le périmétre est "
    tmp = texte.split(" ")
    t=tmp[0]
    l=tmp[1]
    if t == "cercle":
        res+=str(float(l)*math.pi)
    elif t == "rectangle":
        temp=l.split(";")
        res+=str((float(temp[0])+float(temp[1]))*2)
    elif t == "carre" or t == "losange":
        res+=str(float(l)*4)
    elif t == "triangle":
        temp=l.split(";")
        res+=str(float(temp[0])+float(temp[1])+float(temp[2]))
    else:
        res="erreur, type inconnu"
    return str(res)

#utilisation: surface("type l")
def surface(texte):
    res="La surface est "
    tmp = texte.split(" ")
    t=tmp[0]
    l=tmp[1]
    if t == "cercle":
        res+=str(math.pow(float(l),2)*math.pi)
    elif t == "rectangle":
        temp=l.split(";")
        res+=str(float(temp[0])*float(temp[1]))
    elif t == "carre":
        temp=l.split(";")
        res+=str(float(temp[0])*float(temp[0]))
    elif t == "cylindre":
        temp=l.split(";")
        res+=str(math.pi*float(temp[0])*float(temp[1]))
    elif t == "losange" or t == "triangle":
        temp=l.split(";")
        res+=str(float(temp[0])*float(temp[1])/2)
    else:
        res="erreur, type inconnu"
    return str(res)

#utilisation: volume("type l")
def volume(texte):
    res="Le volume est "
    tmp = texte.split(" ")
    t=tmp[0]
    l=tmp[1]
    if t == "sphere":
        res+=str(float(4/3)*math.pi*math.pow(float(l),3))#4/3*pi*r^3
    elif t == "parallelepipede":
        temp=l.split(";")
        res+=str(float(temp[0])*float(temp[1])*float(temp[2]))#a*b*c
    elif t == "cube":
        temp=l.split(";")
        res+=str(float(temp[0])*float(temp[0])*float(temp[0]))#a*b*c
    elif t == "cylindre":
        temp=l.split(";")
        res+=str(math.pi*math.pow(float(temp[0]),2)*float(temp[1]))#pi*R²*h
    else:
        res="erreur, type inconnu"
    return str(res)

#utilisation: calcul(calcul)
def calcul(texte):
    temp = texte.split(" ")
    for i in range(len(temp)-1):
        if temp[i]=="racine":
            temp[i]="math.sqrt("+temp[i+1]+")"
            del temp[i+1]
        if temp[i]=="cosinus":
            temp[i]="math.cos("+temp[i+1]+")"
            del temp[i+1]
        if temp[i]=="sinus":
            temp[i]="math.sin("+temp[i+1]+")"
            del temp[i+1]
        if temp[i]=="tangente":
            temp[i]="math.tan("+temp[i+1]+")"
            del temp[i+1]
    for i in range(len(temp)):
        if re.search("pi",temp[i]):
            temp[i]=temp[i].replace("pi",str(math.pi))
    for i in range(len(temp)):
        if re.search("puissance",temp[i]):
            temp[i]=temp[i].replace("puissance","**")
    equation=" ".join(temp)
    try:
        res=eval(equation)
    except:
        res=resolution1(equation)
    return str(res)


#utilisation: resolution1(equation)
def resolution1(texte):
		res="x="
		i=re.search("[+-/*]?(\d+(\.\d*)?)+x",texte)
		j=re.search("([+-/*](\d+(\.\d*)?)+=)|([+-/*](\d+(\.\d*)?)+$)",texte)
		k=re.search("(=[+-/*]?(\d+(\.\d*)?)+$)|([+-/*]?(\d+(\.\d*)?)+=)",texte)
		try:
			a=i.group(0)[:-1]
		except:
			a=""
		try:
			b=j.group(0)
			if b[-1:] == "=":
				b=b[:-1]
		except:
			b=""
		try:	
			y=k.group(0)
			if y[:1] == "=":
				y=y[1:]
			elif y[-1:] == "=":
				y=y[:-1]
		except:
			y=""
		#print("a="+a+" b="+b+" y="+y)
		if a and b and y:
			if b[:1] == "+":
				t="("+y+"-"+b+")/"+a
			else:
				t="("+y+"+"+b+")/"+a
		elif a and y:
			t=y+"/"+a
		elif b and y:
			if b[:1] == "+":
				t=y+"-"+b
			else:
				t=y+"+"+b			
		elif y:
			t=y
		else:
			t=""
		res=eval(t)
		return str(res)

def run(texte):
    res=""
    if texte == "quit":
        quit()
    if re.search("pythagore",texte):
        f=re.search("[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?(;[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?){1,2}",texte)
        res=pythagore(f.group(0))
    elif re.search("thales",texte):
        f=re.search("[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?(;[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?){2,3}",texte)
        res=thales(f.group(0))
    elif re.search("perimetre",texte):
        try:
            t=re.search("carre|rectangle|cercle|losange|triangle",texte)
            text=t.group(0)
            u=re.search("(\d+)(;\d+)?",texte)
            text+=" "+u.group(0)
            #print(text)
        except:
            text="inconnu"            
        res=perimetre(text)
    elif re.search("surface",texte):
        try:
            t=re.search("carre|cercle|rectangle|cylindre|losange|triangle",texte)
            text=t.group(0)
            u=re.search("(\d+)(;\d+)?",texte)
            text+=" "+u.group(0)
            #print(text)
        except:
            text="inconnu"            
        res=surface(text)
    elif re.search("volume",texte):
        try:
            t=re.search("sphere|parallelepipede|cube|cylindre",texte)
            text=t.group(0)
            u=re.search("(\d+)(;\d+)?",texte)
            text+=" "+u.group(0)
            #print(text)
        except:
            text="inconnu"            
        res=volume(texte)
    else:
        try:
            res=calcul(texte)
        except:
            res="impossible"
    #print(str(res))
    return res

#texte=input("entrer du texte")
#res=run(texte)
#print(res)
