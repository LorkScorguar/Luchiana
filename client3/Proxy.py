#!/usr/bin/python3.3

import urllib.request
import ssl


def connectProxy(type):
    proxy_info = {
    'user' : 'p068679',
    'pass' : 'lucie42',
    'host' : "138.21.88.176",
    'port' : 3128 # or 8080 or whatever
    }

    # build a new opener that uses a proxy requiring authorization
    proxy_support = urllib.request.ProxyHandler({type : "http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxy_info})
    opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler)

    # install it
    urllib.request.install_opener(opener)

    # use it
    """req=urllib.request.Request(url="https://www.google.fr")
    page=urllib.request.urlopen(req).read().decode('utf-8','ignore')
    print(page)"""
    
#connectProxy("https")
