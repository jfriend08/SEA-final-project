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
    param = pickle.loads(str(self.get_argument('param')))
    self.method[type](param, self)
