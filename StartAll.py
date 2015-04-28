#! /usr/bin/env python
import nltk
import math
import re, sys, getopt
import pickle
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from xml.etree.ElementTree import iterparse
import urllib
import socket
import json
from sklearn.feature_extraction.text import TfidfTransformer

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.httpserver import HTTPServer
from tornado.process import fork_processes
from tornado.netutil import bind_sockets

'''
The purpose of StartAll is literally stating all modules!
You will need to have the idea for how many server you need to start up. 
Then, it will to the following proceduer:
1. Find available ports according to the number you specified
2. Indexing, and partision (by hashing or modulo) the files according to your number
3. Fire up all the HTTP servers

The structure of HTTP server is:

                      --> classifier_front(?)   -->
User --> SuperFront   --> searchEng_front       --> searchEng_worker (inclusing IndexServer*3, and DocumentServer*3)
                      --> recom_front           --> recom_worker (inclusing MovieServer*3, and ReviewServer*3)

The purpose of recom_start is to fire up all recom_workers for recommendation, search enigine, and even classifier
Currently involves these parts:
1. get all the ports
2. import recom_front and recom_worker, and fire up those HTTP servers
3. import searchEng_worker and  searchEng_front, and fire up those HTTP servers

recom_worker has two part: 1. movieHandler 2. reviewHandler. 
you have to init it to proper type 
e.g. 
sockets = bind_sockets(port)    
myback_movie = recom_worker.RecommApp('MovieServer', num, port)
myback_movie.app

The purpose of movieHandler is to: 
fetch MovieServers --> get the users --> calculate similarity --> fetch ReviewServers
'''
SuperFront = [] 
masterServer = []
MovieServer = []
ReviewServer = []
IdxServer = []
DocServer = []
ClassifierServer = []


NumSuperFront = 1 #the most frontend server to user
NumMaster = 2 #the masterServer for 1. Search Engine 2. Recommendation System
NumMovie = 3 #for recommendation system
NumReview = 3 #for recommendation system
NumIdx = 3 #for search engine
NumDoc = 3 #for search engine
NumClassifier = 4 #for classifier


def getPorts():
  global SuperFront, masterServer, MovieServer, ReviewServer, IdxServer, DocServer, Baseport, ClassifierServer
  from recommendation import inventory  
  guessPort = 27375 #will start with this port and find the avaliable ports
  # guessPort = 28300 #will start with this port and find the avaliable ports
  allserver = inventory.Inventory()
  Baseport = allserver.callBasePort(guessPort)
  allserver.findPorts( socket.gethostname(), NumSuperFront, NumMaster, NumMovie, NumReview, NumIdx, NumDoc, NumClassifier, Baseport)
  (SuperFront, masterServer, MovieServer, ReviewServer, IdxServer, DocServer, ClassifierServer) = allserver.getAllPorts()   
  allserver.saveJson('./constants') #save all the port info as workers.json to the path you specified 


def main():
  from recommendation import recom_worker, recom_front
  from recommendation import searchEng_worker, searchEng_front  
  from src import localIndexer
  from src import color
  # from src import tomatoCrawler as TC
  C = color.bcolors()

  global masterServer, MovieServer, ReviewServer, IdxServer, DocServer, Baseport
  
  print C.HEADER + "=========== Start Crawling ===========" + C.ENDC
  # TC.main2Genre()

  print C.HEADER + "=========== Find Available Ports ===========" + C.ENDC
  getPorts()

  print C.OKBLUE + "SuperFront:\t" + str(SuperFront) + C.ENDC
  print C.OKBLUE + "masterServer:\t" + str(masterServer) + C.ENDC
  print C.OKBLUE + "MovieServer:\t" + str(MovieServer) + C.ENDC
  print C.OKBLUE + "ReviewServer:\t" + str(ReviewServer) + C.ENDC
  print C.OKBLUE + "IdxServer:\t" + str(IdxServer) + C.ENDC
  print C.OKBLUE + "DocServer:\t" + str(DocServer) + C.ENDC
  print C.OKBLUE + "ClassifierServer:\t" + str(ClassifierServer) + C.ENDC
  
  print C.HEADER + "=========== Start Local Indexing ===========" + C.ENDC
  # localIndexer.ReviewIndexing()

  print C.HEADER + "=========== Fire Up All Servers ===========" + C.ENDC
  uid = fork_processes(NumMaster+NumMovie+NumReview+NumIdx+NumDoc)
  # uid = fork_processes(NumMaster+NumMovie+NumReview+NumIdx+NumDoc)
  
  if uid == 0:
    sockets = bind_sockets(masterServer[uid].split(':')[-1])
    myfront = recom_front.FrontEndApp(MovieServer, ReviewServer)
    server  = myfront.app
  elif uid ==1:
    sockets = bind_sockets(masterServer[uid].split(':')[-1])
    # myfront = searchEng_front.FrontEndApp(IdxServer, DocServer)
    myfront = searchEng_front.FrontEndApp(IdxServer, DocServer)
    server  = myfront.app
  elif uid < NumMaster + NumMovie:
    myIdx = uid - NumMaster
    sockets = bind_sockets(MovieServer[myIdx].split(':')[-1])    
    myback_movie = recom_worker.RecommApp('MovieServer', myIdx, MovieServer[myIdx].split(':')[-1])
    server  = myback_movie.app
  elif uid < NumMaster + NumMovie + NumReview:
    myIdx = uid - NumMovie - NumMaster
    sockets = bind_sockets(ReviewServer[myIdx].split(':')[-1])
    myback_review = recom_worker.RecommApp('ReviewServer', myIdx, ReviewServer[myIdx].split(':')[-1])
    server  = myback_review.app
  elif uid < NumMaster + NumMovie + NumReview + NumIdx:
      myIdx = uid-NumMovie-NumReview-NumMaster
      sockets = bind_sockets(IdxServer[myIdx].split(':')[-1])    
      myback_idx = searchEng_worker.RecommApp('IndexServer', myIdx, IdxServer[myIdx].split(':')[-1])
      server  = myback_idx.app
  elif uid < NumMaster + NumMovie + NumReview + NumIdx + NumDoc:
      myIdx = uid-NumMovie-NumReview-NumIdx-NumMaster
      sockets = bind_sockets(DocServer[myIdx].split(':')[-1])    
      myback_doc = searchEng_worker.RecommApp('DocumentServer', myIdx, DocServer[myIdx].split(':')[-1])
      server  = myback_doc.app

  server.add_sockets(sockets)
  tornado.ioloop.IOLoop.instance().start()




if __name__ == "__main__":        
  main()

