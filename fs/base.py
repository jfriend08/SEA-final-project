import uuid
from tornado.httpclient import HTTPClient, AsyncHTTPClient
from tornado import gen

import fs

try:
  import cPickle as pickle
except:
  import pickle

def formatQuery(host, type, args):
  return '{0}/fs?type={1}&param={2}'.format(host, type, pickle.dumps(args))

def formatEntry(val, indent):
  return '\t' * indent + str(val) + '\n'

def prettyPrint(dic, indent):
  ret = ''
  for key, value in dic.iteritems():
    ret += formatEntry(key, indent)
    if isinstance(value, dict):
      ret += prettyPrint(value, indent+1)
    else:
      ret += formatEntry(value, indent+1)

  return ret

class TableName(object):
  def __init__(self, name):
    self.tableName = name

  @property
  def name(self):
    return self.tableName

'''
Distributed list Object
'''
class DisList(object):
  def __init__(self, initVal=None):
    if initVal:
      self.data = initVal
    else:
      self.data = []

  '''
  Getter
  returns - any, data of this list given idx
  '''
  def __getitem__(self, idx):
    return self.data[idx]

  '''
  Setter
  param idx - int, position to set value
  param val - any, value to be updated
  '''
  def __setitem__(self, idx, val):
    self.data[idx] = val

  '''
  Append val into the last position of list
  param val - any, value to be appended
  '''
  def append(self, val):
    self.data.append(val)

  '''
  Extend the list with new val
  param val - any, value to be extended into list
  '''
  def extend(self, val):
    self.data.extend(val)

  '''
  Remove given value in the list
  param val - any, the value to be removed from list
  param globl - Boolean, Optional value indicating this 
                operation is a global remove or just remove first value in list
  '''
  def remove(self, val, globl=False):
    if globl:
      while val in self.data:
        self.data.remove(val)
    else:
      self.data.remove(val)

  @property
  def length(self):
    return len(self.data)

  def __str__(self):
    ret = '['
    for i in xrange(len(self.data)):
      ret += ' {0} '.format(str(self.data[i]))
    return ret + ']'

'''
Distributed table Object
'''
class DisTable(object):
  def __init__(self, initVal={}, tableName=None):
    if tableName is None:
      self.name = TableName(uuid.uuid4().hex)
    else:
      self.name = TableName(tableName)
    self.master = fs.INVENTORY.getMaster()

    newInitVal = {}
    for key in initVal:
      if isinstance(initVal[key], dict):
        newInitVal[key] = DisTable(initVal[key])
      else:
        newInitVal[key] = initVal[key]

    #Create request to master
    if len(newInitVal.keys()) > 0:
      param = {'tableName': self.name, 'initVal': newInitVal}
      HTTPClient().fetch(formatQuery(self.master, 'create', param))

  @property
  def tableName(self):
    return self.name

  '''
  Getter
  returns - any, data of this table given key
  '''
  def __getitem__(self, key):
    param = {'tableName': self.name, 'key': key}
    res = HTTPClient().fetch(formatQuery(self.master, 'get', param))
    return pickle.loads(res.body)

  '''
  Setter
  param key - key to index updated value
  param val - value to be updated into table
  '''
  def __setitem__(self, key, val):
    param = {'tableName': self.name, 'key': key, 'val': val}
    return HTTPClient().fetch(formatQuery(self.master, 'set', param)).body

  #TODO: Below needs to be implemented

  '''
  Pop data of this key
  param key - The key of data to be removed and returned
  returns - AnyType, whatever value stored with key, None if there's no such value
  '''
  def pop(self, key):
    raise NotImplementedError

  '''
  Determine if table already has this key
  param key - The key to check
  returns - Boolean, True if this key is already in the table, False otherwise
  '''
  def hasKey(self, key):
    raise NotImplementedError

  @property
  def length(self):
    raise NotImplementedError
  '''
  def __str__(self):
    raise NotImplementedError
  '''
