import json
import os

class Inventory(object):
  def __init__(self):
    self.configPath = os.path.join(os.path.dirname(__file__), 'config.json')
    self.servers = []
    try:
      inputFile = open(self.configPath, 'r')
      self.servers = json.load(inputFile)
      inputFile.close()
    except IOError:
      pass

  def attachServer(self, hostName, port):
    self.servers.append('http://{0}:{1}'.format(hostName, port))
    self.dumpInfo()

  def detachServer(self, hostName, port):
    self.servers.remove('http://{0}:{1}'.format(hostName, port))
    self.dumpInfo()

  def getServers(self):
    return self.servers

  @property
  def numServers(self):
    return len(self.servers)

  def __str__(self):
    ret = 'Servers inventory:\n'
    ret += json.dumps(self.servers, indent=4, separators=(',', ': '))
    return ret

  def dumpInfo(self):
    outputFile = open(self.configPath, 'w')
    outputFile.write(json.dumps(self.servers))
    outputFile.close()

  def clearInfo(self):
    try:
      os.remove(self.configPath)
    except:
      pass
