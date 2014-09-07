#!/usr/bin/python3.2
import re
import subprocess
from random import choice

def memorise(save):
	file=open("learn","a")
	for mot in save:
		file.write(mot+"\n")

def learn():
	print("Programme d'apprentissage de Luchiana")
	print("Simuler simplement une conversation entre deux personnes et j'apprendrai")
	i=1
	save=[]
	old=""
	while i > 0:
		if(i%2!=0):
			rep=input(">")
		else:
			rep=input(">>")
		if rep =="quit":
			memorise(save)
			quit()
		rep=rep.strip()	
		if old != "":
			save.append(old+";"+rep)
		old=rep	
		i+=1

def init():
	print("Initialisation en cours")
	actions=[]
	simples=[]
	pronoms=[]
	filesA=["actions-fr","actions-en"]
	filesR=["simple-fr","simple-en","politesse-fr","politesse-en","informatique-fr"]
	filesP=["pronoms-fr","pronoms-en"]
	for file in filesA:
		f=open(file,"r")
		for ligne in f:
			if not re.match("^#",ligne) and not re.match("\n",ligne): #on n'exclut les lignes commentees et les lignes vides
				actions.append(ligne)
		f.close()
	for file in filesR:
		f=open(file,"r")
		for ligne in f:
			if not re.match("^#",ligne) and not re.match("\n",ligne): #on n'exclut les lignes commentees et les lignes vides
				simples.append(ligne)
		f.close()
	for file in filesP:
		f=open(file,'r')
		for ligne in f:
			if not re.match("^#",ligne) and not re.match("\n",ligne): #on n'exclut les lignes commentees et les lignes vides
				pronoms.append(ligne)
		f.close()
	run(actions,simples,pronoms)

def run(actions,simples,pronoms):
	while 1:
		rep=input(">> ") 
		if rep.strip()=="quit":
			quit()
		trouve=False
		anwser="" 
		for expression in actions:
			reponses=""
			temp=expression.split(";")
			mclef=temp[0].split("/")
			commande=temp[1]
			reponses=temp[2].split("/")
			nbmclef=len(mclef)
			j=0
			for i in range(nbmclef):
				if mclef[i]=="?" or mclef[i]=="." or mclef[i]=="*" or mclef[i]=="\"":
					mclef[i]="\""+mclef[i]
				if re.search(mclef[i],rep,re.IGNORECASE):
					j+=1
				if j==nbmclef:
					ans=choice(reponses)
					ans=ans.strip()
					p=subprocess.check_output(commande,shell=True)
					res=p.decode().strip()
					t=ans.split(" ")
					for k in range(len(t)):
						if t[k]=="%REP%":
							t[k]=res
					answer = " ".join(t)+"."
					trouve=True
		for expression in simples:
			temp=expression.split(";")
			mclef=temp[0].split("/")
			reponses=temp[1].split("/")
			nbmclef=len(mclef)
			j=0
			for i in range(nbmclef):
				if mclef[i]=="?" or mclef[i]=="." or mclef[i]=="*" or mclef[i]=="\"":
					mclef[i]="\""+mclef[i]
				if re.search(mclef[i],rep,re.IGNORECASE):
					j+=1
				if j==nbmclef:
					ans=choice(reponses)
					answer=ans.strip()
					trouve=True
		if not trouve:
			answer="je ne comprends pas"
		print("->"+answer+".")

if __name__ == '__main__':
	choix=input("Que voulez vous faire?\n1 me faire évoluer\n2 discuter\n")
	if choix=="1":
		learn()
	else:
		if choix=="2":
			init()
		else:
			print("Je n'ai pas bien compris, mais discutons quand même")
			init()

