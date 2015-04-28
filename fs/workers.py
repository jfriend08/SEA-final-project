import tornado.web
from tornado.concurrent import TracebackFuture as Future
from tornado.httpclient import HTTPResponse

import cStringIO

try:
  import cPickle as pickle
except:
  import pickle

'''
Definition of Worker's file system handler
'''

class FSWorker(object):
  def __init__(self, host):
    self.host = host
    self.tables = {}

  def create(self, param, req):
    tableName = param['tableName']
    initVal = param['initVal']
    self.tables[tableName] = {}
    for key in initVal:
      self.tables[tableName][key] = initVal[key]
    print 'Worker {0} CREATE:'.format(self.host), self.tables[tableName]

    #Release
    fu = Future()
    req.url = self.host
    fu.set_result(HTTPResponse(req, 200, buffer=cStringIO.StringIO('OK')))
    return fu

  def get(self, param, req):
    tableName = param['tableName']
    key = param['key']

    fu = Future()
    req.url = self.host
    fu.set_result(HTTPResponse(req, 200, buffer=cStringIO.StringIO(self.tables[tableName][key])))
    return fu

  def set(self, param, req):
    tableName = param['tableName']
    key = param['key']
    val = param['val']
    self.tables[tableName][key] = val

    fu = Future()
    req.url = self.host
    fu.set_result(HTTPResponse(req, 200, buffer=cStringIO.StringIO('OK')))
    return fu

  def remove(self, param, req):
    tableName = param['tableName']
    key = param['key']
    if not key in self.tables[tableName]:
      return Future().set_result('Key Error')

    if key is None:
      del self.tables[tableName]
    else:
      del self.tables[tableName][key]

    fu = Future()
    req.url = self.host
    fu.set_result(HTTPResponse(req, 200, buffer=cStringIO.StringIO('OK')))
    return Future().set_result('OK')

