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
The purpose of recom_start is to fire up all recom_workers
It involves two parts:
1. get all the ports
2. import recom_front and recom_worker, and fire up those HTTP servers

recom_worker has two part: 1. movieHandler 2. reviewHandler. 
you have to init it to proper type 
e.g. 
sockets = bind_sockets(port)    
myback_movie = recom_worker.RecommApp('MovieServer', num, port)
myback_movie.app

The purpose of movieHandler is to: 
fetch MovieServers --> get the users --> calculate similarity --> fetch ReviewServers
'''

MovieServer=[]
ReviewServer=[]
NumMovie = 3
NumReview = 3

def getPorts():
	global MovieServer, ReviewServer, Baseport
	import inventory	
	allserver = inventory.Inventory()
	Baseport = allserver.callBasePort(20000)
	allserver.findPorts( socket.gethostname(), NumMovie, NumReview, Baseport)
	MovieServer = allserver.getMoviePorts()
	ReviewServer = allserver.getReviewPorts()		
	allserver.saveJson('./')


def main():
	import recom_worker, recom_front
	global MovieServer, ReviewServer, Baseport
	
	getPorts()
	
	print "Baseport:\t" + str(Baseport)
	print "MovieServer:\t" + str(MovieServer)
	print "ReviewServer:\t" + str(ReviewServer)
	
	uid = fork_processes(NumMovie+NumReview+1)
	if uid == 0:
	    sockets = bind_sockets(Baseport)
	    myfront = recom_front.FrontEndApp(MovieServer, ReviewServer)
	    server  = myfront.app
	elif uid < NumMovie + 1:       
	    sockets = bind_sockets(MovieServer[uid-1].split(':')[-1])    
	    myback_movie = recom_worker.RecommApp('MovieServer', uid-1, MovieServer[uid-1].split(':')[-1])
	    server  = myback_movie.app
	elif uid < NumMovie + NumReview + 1:
	    sockets = bind_sockets(ReviewServer[uid-NumMovie-1].split(':')[-1])    
	    myback_review = recom_worker.RecommApp('ReviewServer', uid-NumMovie-1, ReviewServer[uid-NumMovie-1].split(':')[-1])
	    server  = myback_review.app

	server.add_sockets(sockets)
	tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":        
  main()

