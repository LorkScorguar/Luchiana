"""
Module de gestion des tâches planifiées
"""

import datetime

def checkSchedule():
    executeToday=False
    schedFile = open("database/schedule","r")
    today=datetime.datetime.now()
    for line in schedFile:
        schedDay=line.split(";")[0]
        schedTime=lien.split(";")[1]
        func=line.split(";")[2]
        output=line.split(";")[3].strip()
        if schedDay[0]=="m" and today.weekday()==0:
            executeToday=True
        elif schedDay[1]=="t" and today.weekday()==1:
            executeToday=True
        elif schedDay[2]=="w" and today.weekday()==2:
            executeToday=True
        elif schedDay[3]=="t" and today.weekday()==3:
            executeToday=True
        elif schedDay[4]=="f" and today.weekday()==4:
            executeToday=True
        elif schedDay[5]=="s" and today.weekday()==5:
            executeToday=True
        elif schedDay[6]=="s" and today.weekday()==6:
            executeToday=True
        if executeToday and schedTime==today.hour
        res=eval(func)
        output=output.replace("%OUT%",res)
        builtins.sendHandler.sendMsg("N",\
                                     "notif;Planning;"+output)
    return "ok"
