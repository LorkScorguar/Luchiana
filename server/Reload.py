import os
import threading
import time
import imp
import sys

import Cerveau
import Math
import Securite
import System
import Server
import Database
import Mail

def verify():
	i=0 
	dateList=[]
	while 1:
		fileList = ["Cerveau.py","Database.py","FileManager.py","Freebase.py","GPIO.py","Mail.py","Math.py","Securite.py","Server.py","System.py","Tankbot.py","Web.py"]
		j=0
		for file in fileList:
			statbuf = os.stat(file)
			if(i==0):
				ori=statbuf.st_mtime
				dateList.append(ori)
			if(dateList[j]!=statbuf.st_mtime):
				print("rechargement de %s" % file)
				dateList[j]=statbuf.st_mtime
				imp.reload(sys.modules[file[:-3]])
			j+=1
		i+=1
		time.sleep(1)
		
