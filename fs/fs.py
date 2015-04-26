import uuid
from tornado.httpclient import HTTPClient
from tornado import gen

try:
  import cPickle as pickle
except:
  import pickle

def formatQuery(host, type, args):
  for key in args:
    param = '&'.join(['{0}={1}'.format(k, args[k]) for k in args])

  return '{0}/{1}?{2}'.format(host, type, param)

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
  def __init__(self, initVal={}):
    self.name = uuid.uuid4().hex
    #XXX: Need to use sync client
    self.client = HTTPClient()
    #TODO: Sync this with inventory module
    self.master = ''
    #Create request to master
    param['tableName'] = self.name
    param['initVal'] = pickle.dumps(initVal)
    self.client.fetch(formatQuery(self.master, 'create', param))

  '''
  Getter
  returns - any, data of this table given key
  '''
  def __getitem__(self, key):
    param = {'tableName': self.name, 'key': key}
    return self.client.fetch(formatQuery(self.master, 'get', param)).body

  '''
  Setter
  param key - key to index updated value
  param val - value to be updated into table
  '''
  def __setitem__(self, key, val):
    param = {'tableName': self.name, 'key': key, 'val': val}
    return self.client.fetch(formatQuery(self.master, 'set', param)).body

  #TODO: Below needs to be implemented

  '''
  Pop data of this key
  param key - The position of data to be removed and returned
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

  def __str__(self):
    raise NotImplementedError
