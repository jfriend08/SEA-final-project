import tornado.web

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

  def create(self, param, res):
    tableName = param['tableName']
    initVal = param['initVal']
    self.tables[tableName] = {}
    for key in initVal:
      self.tables[tableName][key] = initVal[key]
    print 'Worker {0} CREATE:'.format(self.host), self.tables[tableName]

  def get(self, param, res):
    tableName = param['tableName']
    key = param['key']
    res.write(self.tables[tableName][key])

  def set(self, param, res):
    tableName = param['tableName']
    key = param['key']
    val = param['val']
    self.tables[tableName][key] = val

  def remove(self, param, res):
    tableName = param['tableName']
    key = param['key']
    if not key in self.tables[tableName]:
      return

    if key is None:
      del self.tables[tableName]
    else:
      del self.tables[tableName][key]
