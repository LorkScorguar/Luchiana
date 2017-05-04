#!/usr/bin/python3.3
"""
Main module
"""

import threading
import time
import builtins

import Cerveau
import Securite
import System
import Reload
import Server
import Proxy
import Config

if __name__ == '__main__':
    Proxy.connectProxy("http")
    STARTTIME = time.time()
    print("Initialisation en cours")
    HOST, PORT = Config.address, Config.port
    LS = Server.ThreadedTCPServer((HOST, PORT), Server.ThreadedTCPRequestHandler)
    Securite.init()
    #Cerveau.init()
    builtins.init = 0
    SERVER_THREAD = threading.Thread(target=LS.serve_forever)
    SERVER_THREAD.start()
    print("initialisation réalisé en "+str(time.time()-STARTTIME)+"sec")
    print('Serving')
#    MON = System.MyMonitoringThread('Monitoring')
#    MON.start()
    REL = threading.Thread(None, Reload.verify, None)
    REL.start()
