"""
attention à ne compter que le nombre de mots entre / et pas entre |
"""
import re
import hashlib
from random import choice
import getpass

user_file="server/database/users"
########################
# Users modifications  #
########################
def searchUser(username):
	file=open(user_file,'r')
	for line in file:
		temp=line.split(";")
		user=temp[0]
		password=temp[1]
		if username == user:
			answer=password.strip()
			break
		else:
			answer="invalide"
	return answer

def addUser(username,password):
	save=[]
	file=open(user_file,'a')
	file.write(username+";"+hashlib.sha224(password.encode('utf-8')).hexdigest()+";user")
	return username+" a ete ajoute aux utilisateurs"

def updateUser(username,password,newPassword):
	save=[]
	file=open(user_file,'r')
	oldPassword=searchUser(username)
	if oldPassword==hashlib.sha224(password.encode('utf-8')).hexdigest():
		for line in file:
			save.append(line.strip())
		file=open(user_file,'w')
		for i in range(len(save)):
			temp=save[i].split(";")
			if temp[0] == username:
				save[i]=username+";"+hashlib.sha224(password.encode('utf-8')).hexdigest()+temp[2]
		for i in range(len(save)):
			file.write(save[i]+"\n")
		answer="mot de passe mis a jour pour "+username
	else:
		answer="erreur, les mots de passes ne correspondent pas"
	return answer

def removeUser(username):
	save=[]
	file=open(user_file,'r')
	for line in file:
		save.append(line.strip())
	file=open(user_file,'w')
	for i in range(len(save)):
		temp=save[i].split(";")
		if temp[0] == username:
			del save[i]
	for i in range(len(save)):
		file.write(save[i]+"\n")
	return "utilisateur "+username+" supprime"

def run():
    choix=input("Que voulez-vous faire?\n1-Ajouter un utilisateur\n2-Mettre a jour un utilisateur\n3-Supprimer un utilisateur\n")
    if choix == "1":
        username=input("Entrer le nom de l'utilisateur: ")
        password=getpass.getpass("Entrer le mot de passe de cet utilisateur: ")
        password2=getpass.getpass("Re-entrer le mot de passe: ")
        verif=searchUser(username)
        if password==password2 and verif=="invalide":
            r=addUser(username,password)
            print(r)
        elif password!=password2:
            print("Les mots de passes ne sont pas identiques")
        else:
            print("L'utilisateur existe deja")
    elif choix == "2":
        username=input("Entrer le nom de l'utilisateur: ")
        password=getpass.getpass("Entrer le mot de passe actuel de cet utilisateur: ")
        password2=getpass.getpass("Entrer le nouveau mot de passe: ")
        password3=getpass.getpass("Re-entrer le nouveau mot de passe: ")
        if password2==password3:
            r=updateUser(username,password,password2)
            print(r)
        else:
            print("Les mots de passes ne sont pas identiques")
    elif choix == "3":
        username=input("Entrer le nom de l'utilisateur: ")
        r=removeUser(username)        
        print(r)
    else:
        print("Choix incorrect")

#run()
