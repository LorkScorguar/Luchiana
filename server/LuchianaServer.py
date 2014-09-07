#!/usr/bin/python3.3
import Cerveau
import Securite
import System
import Reload
import Server
import threading
import time
import builtins
import Mail
import time
import Proxy
import Config

if __name__ == '__main__':
    Proxy.connectProxy("http")
    starttime=time.time()
    print("Initialisation en cours")
    HOST, PORT = Config.address, Config.port
    LS = Server.ThreadedTCPServer((HOST, PORT), Server.ThreadedTCPRequestHandler)
    Securite.init()
    Cerveau.init()
    builtins.init=0
    server_thread = threading.Thread(target=LS.serve_forever)
    server_thread.start()
    print("initialisation réalisé en "+str(time.time()-starttime)+"sec")
    print('Serving')
#    a=System.MyMonitoringThread('Monitoring')
#    a.start()
    b=threading.Thread(None,Reload.verify,None)
    b.start()


