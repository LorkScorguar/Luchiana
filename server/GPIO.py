"""
module pour la gestion des ports GPIO en Python
"""

import subprocess

def active(port, mode):
    """active le port"""
    subprocess.check_output("gpio mode "+str(port)+" "+mode, shell=True)
    return 0

def allume(port):
    """allume le port"""
    subprocess.check_output("gpio write "+str(port)+" 1", shell=True)
    return 0

def eteint(port):
    """eteint le port"""
    subprocess.check_output("gpio write "+str(port)+" 0", shell=True)
    return 0

def getValue(port):
    """Récupére la valeur du port"""
    subprocess.check_output("gpio read "+str(port), shell=True)
    return 0
