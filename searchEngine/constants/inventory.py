import json
import os
import hashlib, getpass

class Inventory(object):
  def __init__(self):
    self.indexers = []
    self.documents = []
    # self.loadServer()

  def getIndexers(self):
    return self.indexers

  def getDocuments(self):
    return self.documents

  def findPorts(self, host, NIdx, NDoc, Base):    
    for i in range(0, NIdx):
      port = self.callBasePort(Base)      
      self.indexers.append('http://{0}:{1}'.format(host,port))
      Base = port

    for i in range(0, NDoc):
      port = self.callBasePort(Base)
      self.documents.append('http://{0}:{1}'.format(host,port))
      Base = port

  def callBasePort(self, minPort):    
    maxPort = 49152      
    basePort = int(hashlib.md5(getpass.getuser()).hexdigest()[:8], 16) % (maxPort - minPort) + minPort    
    return basePort

  

  # def loadServer(self):
  #   self.indexers = json.load(open(os.path.dirname(__file__)+"/servers.json", "r"))['indexes']
  #   self.documents = json.load(open(os.path.dirname(__file__)+"/servers.json", "r"))["documents"]  