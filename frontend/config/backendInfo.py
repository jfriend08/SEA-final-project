import json
import os.path

class BackendInfo:
  def __init__(self, path):
    #path = os.path.dirname(__file__) + '/../' +path
    #print path
    temp = json.load(open(path, "r"))
    temp = temp['master']
    print temp
    self.info = {}
    self.info['classifier'] = []
    self.info['classifier'].append(temp[0])
    self.info['search'] = []
    self.info['search'].append(temp[1])
    self.info['recommend'] = []
    self.info['recommend'].append(temp[2])
    print self.info

if __name__ == "__main__":
  backend = BackendInfo('config/worker_info.json')
  print backend.info