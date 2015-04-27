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

  def create(self, tableName, initVal={}):
    self.tables[tableName] = {}
    for key in initVal:
      self.tables[tableName][str(key)] = initVal[key]
    print 'Worker {0} CREATE:'.format(self.host), self.tables[tableName]

  def get(self, tableName, key, res):
    res.write(self.tables[tableName][str(key)])

  def set(self, tableName, key, val):
   self.tables[tableName][key] = val

  def remove(self, tableName, key=None):
    if not key in self.tables[tableName]:
      return

    if key is None:
      del self.tables[tableName]
    else:
      del self.tables[tableName][key]
