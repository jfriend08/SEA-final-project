import tornado.httpserver
import tornado.ioloop
import tornado.web
import hashlib
import socket
import getpass

import json

from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.options import define, options

'''
The purpose of movieHandler is to: 
fetch MovieServers --> get the users --> calculate similarity --> fetch ReviewServers
'''


ports=[]
ports_movie = []
ports_review = []


class Application(tornado.web.Application):
  def __init__(self):
    handlers = [(r"/recom", recomHandler)]
    tornado.web.Application.__init__(self, handlers)




class recomHandler(tornado.web.RequestHandler):
  @gen.coroutine
  def get(self):
    userID = self.get_argument('user', None)





class FrontEndApp(object):
  def __init__(self, MovieServers, ReviewServer):
    global ports_index, ports_Doc
    ports_movie = MovieServers
    ports_review = ReviewServer
    self.app = tornado.httpserver.HTTPServer(Application() )        
