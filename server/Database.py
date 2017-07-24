"""
Module de gestion de la base de données
"""
import hashlib
import getpass
import os

USER_FILE = os.path.dirname(__file__)+"/database/users"
########################
# Users modifications  #
########################
def searchUser(username):
    """Recherche d'un utilisateur"""
    file = open(USER_FILE, 'r')
    for line in file:
        temp = line.split(";")
        user = temp[0]
        password = temp[1]
        if username == user:
            answer = password.strip()
            break
        else:
            answer = "invalide"
    return answer

def addUser(username, password):
    """Ajout d'un utilisateur"""
    file = open(USER_FILE, 'a')
    file.write(username+";"+\
               hashlib.sha224(password.encode('utf-8')).hexdigest()+";user")
    return username+" a ete ajoute aux utilisateurs"

def updateUser(username, password, newPassword):
    """Modification d'un utilisateur"""
    save = []
    file = open(USER_FILE, 'r')
    oldPassword = searchUser(username)
    if oldPassword == hashlib.sha224(password.encode('utf-8')).hexdigest():
        for line in file:
            save.append(line.strip())
        file = open(USER_FILE, 'w')
        for i in range(len(save)):
            temp = save[i].split(";")
            if temp[0] == username:
                save[i] = username+";"+\
                          hashlib.sha224(\
                          newPassword.encode('utf-8')).hexdigest()+\
                          temp[2]
        for i in range(len(save)):
            file.write(save[i]+"\n")
        answer = "mot de passe mis a jour pour "+username
    else:
        answer = "erreur, les mots de passes ne correspondent pas"
    return answer

def removeUser(username):
    """Suppression d'un utilisateur"""
    save = []
    file = open(USER_FILE, 'r')
    for line in file:
        save.append(line.strip())
    file = open(USER_FILE, 'w')
    for i in range(len(save)):
        temp = save[i].split(";")
        if temp[0] == username:
            del save[i]
    for i in range(len(save)):
        file.write(save[i]+"\n")
    return "utilisateur "+username+" supprime"

def run():
    """Fonction principale"""
    choix = input("Que voulez-vous faire?\n1-Ajouter un utilisateur\n"\
                  "2-Mettre a jour un utilisateur\n"\
                  "3-Supprimer un utilisateur\n4-Rien\n")
    if choix == "1":
        username = input("Entrer le nom de l'utilisateur: ")
        password = getpass.getpass("Entrer le mot de passe"\
                                   " de cet utilisateur: ")
        password2 = getpass.getpass("Re-entrer le mot de passe: ")
        verif = searchUser(username)
        if password == password2 and verif == "invalide":
            res = addUser(username, password)
            print(res)
        elif password != password2:
            print("Les mots de passes ne sont pas identiques")
        else:
            print("L'utilisateur existe deja")
    elif choix == "2":
        username = input("Entrer le nom de l'utilisateur: ")
        password = getpass.getpass("Entrer le mot de passe actuel "\
                                   "de cet utilisateur: ")
        password2 = getpass.getpass("Entrer le nouveau mot de passe: ")
        password3 = getpass.getpass("Re-entrer le nouveau mot de passe: ")
        if password2 == password3:
            res = updateUser(username, password, password2)
            print(res)
        else:
            print("Les mots de passes ne sont pas identiques")
    elif choix == "3":
        username = input("Entrer le nom de l'utilisateur: ")
        res = removeUser(username)
        print(res)
    elif choix == "4":
        print("Sans utilisateur, vous ne pourrez rien faire\n"\
              "Vous pouvez relancer ce module a tout moment "\
              "en appellant Database.py")
    else:
        print("Choix incorrect")

if __name__ == '__main__':
    run()
