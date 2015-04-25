import tornado.httpserver
import tornado.ioloop
import tornado.web
import hashlib
import socket
import getpass
import os, re, math
import json
import pickle
import urllib
import uuid
from nltk.tokenize import RegexpTokenizer

from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.options import define, options
import subprocess
from operator import mul


'''
recom_worker has two part: 1. movieHandler 2. reviewHandler. 
you have to init it to proper type 
e.g. 
sockets = bind_sockets(port)    
myback_movie = recom_worker.RecommApp('MovieServer', num, port)
myback_movie.app
'''


class Application(tornado.web.Application):
    def __init__(self, server):
      if (server == 'IndexServer'):
        handlers = [(r"/IndexServer", movieHandler)]
      elif (server == 'DocumentServer'):
        handlers = [(r"/review", reviewHandler)]
      else:
        raise NameError('wrong server name')
      tornado.web.Application.__init__(self, handlers)  



class movieHandler(tornado.web.RequestHandler):
  @gen.coroutine            
  def get(self):
    self.write("movieHandler")

class reviewHandler(tornado.web.RequestHandler):
  @gen.coroutine            
  def get(self):
    self.write("reviewHandler")




class RecommApp(object):
  def __init__(self, serverType, serverNum, port):    
    # if (serverType=='MovieServer'):
    #   pass
    #   # path = os.path.dirname(__file__) + '/../pickle/indexServer' + str(serverNum)
    # elif (serverType=='ReviewServer'):
    #   pass
    #   # path = os.path.dirname(__file__) + '/../pickle/docServer' + str(serverNum)
    # else:
    #   raise NameError('path error')

    self.app = tornado.httpserver.HTTPServer(Application(serverType) ) 






