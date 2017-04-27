#!/usr/bin/python3.3

import urllib.request
import ssl


def connectProxy(type):
    proxy_info = {
    'host' : "lx5804.res.jcdecaux.org",
    'port' : 8000 # or 8080 or whatever
    }

    # build a new opener that uses a proxy requiring authorization
    proxy_support = urllib.request.ProxyHandler({type : "http://%(host)s:%(port)d" % proxy_info})
    opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler)

    # install it
    urllib.request.install_opener(opener)

    # use it
    """req=urllib.request.Request(url="https://www.google.fr")
    page=urllib.request.urlopen(req).read().decode('utf-8','ignore')
    print(page)"""
    
#connectProxy("https")
