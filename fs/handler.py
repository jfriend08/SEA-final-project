import tornado.web

try:
  import cPickle as pickle
except:
  import pickle

class FSHandler(tornado.web.RequestHandler):
  def initialize(self, processObj):
    self.processObj = processObj
    #Registered methods
    self.method = {
      'create': self.processObj.create,
      'get': self.processObj.get,
      'set': self.processObj.set,
      'remove': self.processObj.remove
    }

  def get(self):
    type = self.get_argument('type')
    tableName = self.get_argument('tableName')

    try:
      key = self.get_argument('key')
    except tornado.web.MissingArgumentError:
      key = None

    if type == 'create':
      initVal = pickle.loads(str(self.get_argument('initVal')))
      self.method[type](tableName, initVal)
    elif type == 'set':
      val = self.get_argument('val')
      self.method[type](tableName, key, val)
    elif type == 'get':
      self.method[type](tableName, key, self)
    else:
      self.method[type](tableName, key)


