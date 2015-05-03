import json
import os
import hashlib, getpass

'''
The purpose of inventory is to help recom_start to find out the available ports
and save the port if needed
Usage:
  import inventory as tool
  allserver = tool.Inventory()
  Baseport = allserver.callBasePort(20000)
  allserver.findPorts(socket.gethostname(), NumMovie, NumReview, Baseport)
  MovieServer = allserver.getMoviePorts()
  ReviewServer = allserver.getReviewPorts()   
  allserver.saveJson(path)
'''


class Inventory(object):
  def __init__(self):
    self.SuperFront = []
    self.master = []
    self.movie = []
    self.review = []
    self.Index = []
    self.Doc = []    
    self.Classifier = []

  def getMoviePorts(self):
    return self.movie

  def getReviewPorts(self):
    return self.review

  def getAllPorts(self):
    return (self.SuperFront, self.master, self.movie, self.review, self.Index, self.Doc, self.Classifier)

  def findPorts(self, host, NSuper, NMaster, NMov, NRev, NIdx, NDoc, NClas, Base):    
    for i in xrange(NSuper):
      port = self.callBasePort(Base)      
      self.SuperFront.append('http://{0}:{1}'.format(host,port))
      Base = port
    for i in xrange(NMaster):
      port +=1
      # port = self.callBasePort(Base)      
      self.master.append('http://{0}:{1}'.format(host,port))
      Base = port
    for i in xrange(NMov):
      port +=1
      # port = self.callBasePort(Base)      
      self.movie.append('http://{0}:{1}'.format(host,port))
      Base = port
    for i in xrange(NRev):
      port +=1
      # port = self.callBasePort(Base)
      self.review.append('http://{0}:{1}'.format(host,port))
      Base = port
    for i in xrange(NIdx):
      port +=1
      # port = self.callBasePort(Base)
      self.Index.append('http://{0}:{1}'.format(host,port))
      Base = port
    for i in xrange(NDoc):
      port +=1
      # port = self.callBasePort(Base)
      self.Doc.append('http://{0}:{1}'.format(host,port))
      Base = port    
    for i in xrange(NClas):
      port +=1
      # port = self.callBasePort(Base)
      self.Classifier.append('http://{0}:{1}'.format(host,port))
      Base = port    
    # print str(self.master)+str(self.movie)+str(self.review)+str(self.Index)+str(self.Doc)

  def callBasePort(self, minPort):    
    maxPort = 49152          
    basePort = int(hashlib.md5(getpass.getuser()).hexdigest()[:8], 16) % (maxPort - minPort) + minPort    
    return basePort
  
  def saveJson(self, path):    
    result = {"superfront":[url for url in self.SuperFront]
    , "master":[url for url in self.master]
    , "movie": [url for url in self.movie]
    , "review": [url for url in self.review]
    , "index": [url for url in self.Index]
    , "doc": [url for url in self.Doc]
    , "classifier":[url for url in self.Classifier]
    }
    PATH = str(path) + "/workers.json"
    f = open( PATH, "w")
    f.write(json.dumps(result))
    f.close()




