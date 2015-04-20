
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
Distributed table Object
'''
class DisTable(object):
  def __init__(self, initVal=None):
    if initVal:
      self.data = initVal
    else:
      self.data = {}

  '''
  Getter
  returns - dict, Whole data of this table as dict
  '''
  def __getitem__(self, key):
    return self.data[key]

  '''
  Setter
  param key - key to index updated value
  param val - value to be updated into table
  '''
  def __setitem__(self, key, val):
    print 'key:', key
    print 'val:', val
    self.data[key] = val

  '''
  Pop data of this key
  param key - The position of data to be removed and returned
  returns - AnyType, whatever value stored with key
  '''
  def pop(self, key):
    try:
      return self.data.pop(key)
    except KeyError:
      pass

  '''
  Determine if table already has this key
  param key - The key to check
  returns - Boolean, True if this key is already in the table, False otherwise
  '''
  def hasKey(self, key):
    return key in self.data

  @property
  def length(self):
    return len(self.data.keys())

  def __str__(self):
    return prettyPrint(self.data, 0)
