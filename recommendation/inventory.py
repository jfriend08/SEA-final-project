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
    self.movie = []
    self.review = []
    # self.loadServer()

  def getMoviePorts(self):
    return self.movie

  def getReviewPorts(self):
    return self.review

  def findPorts(self, host, NMov, NRev, Base):    
    for i in range(0, NMov):
      port = self.callBasePort(Base)      
      self.movie.append('http://{0}:{1}'.format(host,port))
      Base = port

    for i in range(0, NRev):
      port = self.callBasePort(Base)
      self.review.append('http://{0}:{1}'.format(host,port))
      Base = port

  def callBasePort(self, minPort):    
    maxPort = 49152      
    basePort = int(hashlib.md5(getpass.getuser()).hexdigest()[:8], 16) % (maxPort - minPort) + minPort    
    return basePort
  
  def saveJson(self, path):
    result = {"movie": [url for url in self.movie], "review": [url for url in self.review]}
    PATH = str(path) + "/workers.json"
    f = open( PATH, "w")
    f.write(json.dumps(result))
    f.close()