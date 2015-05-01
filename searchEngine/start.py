import nltk
import math
import re, sys
import pickle
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from xml.etree.ElementTree import iterparse
import urllib
import socket
from sklearn.feature_extraction.text import TfidfTransformer

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.httpserver import HTTPServer
from tornado.process import fork_processes
from tornado.netutil import bind_sockets

from constants import color
bcolors = color.bcolors()


numIdx = 3
numDoc = 3

# deciding ports
from constants import inventory
allserver = inventory.Inventory()
Baseport = allserver.callBasePort(10000)
allserver.findPorts( socket.gethostname(), numIdx, numDoc, Baseport)
Idxservers = allserver.getIndexers()
Docservers = allserver.getDocuments()

# print basic port information
print bcolors.HEADER + "====== BASIC INFO ======" + bcolors.ENDC
print bcolors.OKGREEN + "num of Index Server: " + bcolors.ENDC + bcolors.OKBLUE + str(numIdx) + bcolors.ENDC
print bcolors.OKGREEN + "num of Document Server: " + bcolors.ENDC + bcolors.OKBLUE + str(numDoc) + bcolors.ENDC
print bcolors.OKGREEN + 'Front end will listen to: ' + bcolors.ENDC + bcolors.OKBLUE + 'http://{}:{}'.format(socket.gethostname(), Baseport)  + bcolors.ENDC + "\n"

# # start indexer and save it properly 
# from indexer import indexer
# print bcolors.HEADER + "====== PREPARATION ======" + bcolors.ENDC
# myindexer=indexer.Indexer(Idxservers, Docservers)
# myindexer.genNum()
# myindexer.getXML('./constants/info_ret.xml', Idxservers, Docservers)

# start working
print "\n" + bcolors.HEADER + '====== START FORKING ======'+ bcolors.ENDC
from backend import back
from frontend import front
uid = fork_processes(numIdx+numDoc+1)
if uid == 0:
    sockets = bind_sockets(Baseport)
    myfront = front.FrontEndApp(Idxservers, Docservers)
    server  = myfront.app
elif uid < numIdx + 1:       
    sockets = bind_sockets(Idxservers[uid-1].split(':')[-1])    
    myback_idx = back.BackEndApp('indexServer', uid-1, Idxservers[uid-1].split(':')[-1])
    server  = myback_idx.app
elif uid < numIdx + numDoc + 1:
    sockets = bind_sockets(Docservers[uid-numIdx-1].split(':')[-1])    
    myback_doc = back.BackEndApp('docServer', uid-numIdx-1, Docservers[uid-numIdx-1].split(':')[-1])
    server  = myback_doc.app

server.add_sockets(sockets)
tornado.ioloop.IOLoop.instance().start()




