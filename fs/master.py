from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import tornado.ioloop

from fs import DisTable

try:
  import cPickle as pickle
except:
  import pickle

def formatQuery(host, type, args):
  for key in args:
    param = '&'.join(['{0}={1}'.format(k, args[k]) for k in args])

  return '{0}/{1}?{2}'.format(host, type, param)

class FSMaster(object):
  def __init__(self, workers):
    self.workers = workers
    self.num_workers = len(workers)
    self.tables = DisTable()
    self.client = AsyncHTTPClient()

  @gen.coroutine
  def create(self, tableName, initVal={}):
    if self.tables.hasKey(tableName):
      raise KeyError, 'Table name already existed'

    futures = []
    for worker in self.workers:
      param = {'tableName': tableName}
      if len(initVal.keys()) > 0:
        param['initVal'] = pickle.dumps(initVal)
      futures.append(self.client.fetch(formatQuery(worker, 'create', param)))

    self.tables[tableName] = initVal

  @gen.coroutine
  def get(self, tableName, key, res):
    if not self.tables.hasKey(tableName):
      raise KeyError, 'Table not found!'
    worker = self.workers[hash(key) % self.num_workers]
    param = {'tableName': tableName, 'key': key}

    response = yield self.client.fetch(formatQuery(worker, 'get', param))
    res.write(response.body)

  @gen.coroutine
  def set(self, tableName, key, val):
    if not self.tables.hasKey(tableName):
      raise KeyError, 'Table not Found!'
    worker = self.workers[hash(key) % self.num_workers]
    param = {'tableName': tableName, 'key': key, 'val': pickle.dumps(val)}

    futures = []
    futures.append(self.client.fetch(formatQuery(worker, 'set', param)))

  @gen.coroutine
  def remove(self, tableName, key=None):
    if not self.tables.hasKey(tableName):
      #Silently fails
      return

    param = {'tableName': tableName, 'key': key}
    futures = []
    for worker in self.workers:
      futures.append(self.client.fetch(formatQuery(worker, 'remove', param)))
    if key is None:
      del self.tables[tableName]
