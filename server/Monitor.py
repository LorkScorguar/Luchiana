"""This module is used to monitor some resources and
tell user when something happened
- Check for anomally (zombie, cpu/ram usage, high temperature)
- Check emails
- Check new post/article on some websites
"""
import threading
import builtins
import subprocess

import Mail

class Monitor():

    def memUsage(self):
        self.process = subprocess.Popen("ps aux|awk 'NR > 0 {s+=$4}; END {print s}'", shell=True, stdout=subprocess.PIPE,)
        self.stdout_list = self.process.communicate()[0].split(b'\n')
        return float(self.stdout_list[0])

    def cpuUsage(self):
#à corriger, ne correspond pas ni à conky ni à htop
        self.process = subprocess.Popen("ps aux|awk 'NR > 0 {s+=$3}; END {print s}'", shell=True, stdout=subprocess.PIPE,)
        self.stdout_list = self.process.communicate()[0].split(b'\n')
        return float(self.stdout_list[0])

    def checkTemp(self):
            self.process = subprocess.Popen("sensors | grep temp1 | awk '{print $2}' | sed 's/°C//g' | sed 's/+//g'",  shell=True,stdout=subprocess.PIPE,)
            self.stdout_list = self.process.communicate()[0].split(b'\n')
            t=""
            for i in range(len(self.stdout_list)):
                if len(self.stdout_list[i])>0:
                    t+=" "+str(self.stdout_list[i].decode())+"°C"
            return t

    def checkForZombie(self):
            self.process = subprocess.Popen("ps aux | grep -w Z | grep -v 'grep' | awk '{print $2}'", shell=True, stdout=subprocess.PIPE,)
            self.stdout_list = self.process.communicate()[0].split(b'\n')
            z=""
            for i in range(len(self.stdout_list)):
                if len(self.stdout_list[i])>0:
                    z+=" "+str(self.stdout_list[i].decode())
            return z

    def checkMail(self,addr):
        res=Mail.checkGmail()
        return res

    def updateFiledb():
        res=subprocess.check_output("sudo updatedb")

class MyMonitoringThread(threading.Thread):
    def __init__(self, nom = ''):
        threading.Thread.__init__(self)
        self.nom = nom
        self._stopevent = threading.Event( )

    def run(self):
        mon=Monitor()
        while not self._stopevent.isSet():
            used_cpu=mon.cpuUsage()
            used_mem=mon.memUsage()
            received_mail=mon.checkMail()
            if builtins.init==1:
                if used_mem > 80:
                    builtins.sendHandler.sendMsg("N","notif;Systeme;Ram utilisee a "+str(used_mem)+"%;4")
                if used_cpu > 80:
                    builtins.sendHandler.sendMsg("N","notif;Systeme;Cpu utilise a "+str(used_cpu)+"%;4")
                if received_mail > 0:
                    builtins.sendHandler.sendMsg("N","notif;Systeme;Vous avez "+received_mail+" nouveaux mails")
            self._stopevent.wait(60)
        print("le thread "+self.nom+" s'est termine proprement")

    def stop(self):
        self._stopevent.set( )
