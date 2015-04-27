from tornado.httpclient import AsyncHTTPClient
from tornado import gen

import tornado.web

try:
  import cPickle as pickle
except:
  import pickle

'''
Definition of Master's file system handler
'''

def formatQuery(host, type, args):
  for key in args:
    param = '&'.join(['{0}={1}'.format(k, args[k]) for k in args])

  return '{0}/fs?type={1}&{2}'.format(host, type, param)

class FSMaster(object):
  def __init__(self, workers):
    self.workers = workers
    self.num_workers = len(workers)
    self.tables = {}
    self.client = AsyncHTTPClient()

  @gen.coroutine
  def create(self, tableName, initVal={}):
    if tableName in self.tables:
      raise KeyError, 'Table name already existed'

    print 'MASTER CREATE:', initVal

    vals = {}
    for worker_id in xrange(self.num_workers):
      vals[worker_id] = {}
    for key in initVal:
      worker = hash(str(key)) % self.num_workers
      vals[worker][str(key)] = initVal[key]

    futures = []
    for worker_id in xrange(self.num_workers):
      param = {'tableName': tableName, 'initVal': pickle.dumps(vals[worker_id])}
      futures.append(self.client.fetch(formatQuery(self.workers[worker_id], 'create', param)))

    self.tables[tableName] = True

  @gen.coroutine
  def get(self, tableName, key, res):
    if not tableName in self.tables:
      raise KeyError, 'Table not found!'
    worker = self.workers[hash(str(key)) % self.num_workers]
    param = {'tableName': tableName, 'key': key}

    print 'MASTER GET: {0}.{1} from {2}'.format(tableName, key, worker)

    response = yield self.client.fetch(formatQuery(worker, 'get', param))
    res.write(response.body)

  @gen.coroutine
  def set(self, tableName, key, val):
    if not tableName in self.tables:
      raise KeyError, 'Table not Found!'
    worker = self.workers[hash(key) % self.num_workers]
    param = {'tableName': tableName, 'key': key, 'val': pickle.dumps(val)}

    print 'MASTER SET: {0}.{1} with {2} to {3}'.format(tableName, key, val, worker)

    futures = []
    futures.append(self.client.fetch(formatQuery(worker, 'set', param)))

  @gen.coroutine
  def remove(self, tableName, key):
    if not tableName in self.tables:
      #Silently fails
      return

    param = {'tableName': tableName, 'key': key}
    futures = []
    for worker in self.workers:
      futures.append(self.client.fetch(formatQuery(worker, 'remove', param)))
    if key is None:
      del self.tables[tableName]
