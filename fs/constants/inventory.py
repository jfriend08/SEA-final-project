import json
import os

class Inventory(object):
  def __init__(self):
    self.configPath = os.path.join(os.path.dirname(__file__), 'config.json')
    self.servers = {'master': '', 'workers': []}
    try:
      inputFile = open(self.configPath, 'r')
      self.servers = json.load(inputFile)
      inputFile.close()
    except IOError:
      pass

  def setMaster(self, hostName, port):
    self.servers['master'] = 'http://{0}:{1}'.format(hostName, port)
    self.dumpInfo()

  def attachServer(self, hostName, port):
    self.servers['workers'].append('http://{0}:{1}'.format(hostName, port))
    self.dumpInfo()

  def detachServer(self, hostName, port):
    self.servers.remove('http://{0}:{1}'.format(hostName, port))
    self.dumpInfo()

  def getMaster(self):
    return self.servers['master']

  def getWorkers(self):
    return self.servers['workers']

  @property
  def numWorkers(self):
    return len(self.servers['workers'])

  def __str__(self):
    ret = 'Servers inventory:\n'
    ret += 'Master: {0}\n'.format(self.servers['master'])
    ret += json.dumps(self.servers['workers'], indent=4, separators=(',', ': '))
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
