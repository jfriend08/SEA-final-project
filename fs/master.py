from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import tornado.ioloop

class FSMaster(object):
  def __init__(self, workers):
    self.workers = workers
    self.num_workers = len(workers)
    self.tables = {}

  @gen.coroutine
  def create(self, tableName, initVal={}):
    if tableName in self.tables:
      raise KeyError, 'Table name already existed'

    for worker in self.workers:
      #TODO: Send request to create table
      pass

    self.tables[tableName] = initVal

  @gen.coroutine
  def get(self, tableName, key):
    if not tableName in self.tables:
      raise KeyError, 'Table not found!'
    worker = self.workers[hash(key) % self.num_workers]
    #TODO: GET to worker

  @gen.coroutine
  def set(self, tableName, key, val):
    if not tableName in self.tables:
      raise KeyError, 'Table not Found!'
    worker = self.workers[hash(key) % self.num_workers]
    #TODO: POST to worker

  @gen.coroutine
  def remove(self, tableName, key=None):
    if not tableName in self.tables:
      #Silently fails
      return

    #TODO: SET to workers
    if key is None:
      del self.tables[tableName]
