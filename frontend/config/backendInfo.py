import json

class BackendInfo:
  def __init__(self, path):
    self.info = json.load(open(path, "r"))

if __name__ == "__main__":
  backend = BackendInfo('config/worker_info.json')
  print backend.info