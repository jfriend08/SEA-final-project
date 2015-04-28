# tornado
from tornado.process import fork_processes
import tornado.ioloop
import tornado.web
# package
from config import inventory
from backend import offline
# 
import sys

if __name__ == "__main__":
  try: 
    path =  sys.argv[1]
  except IndexError:
    path = 'classifier_worker_address.json'

  BASE_PORT = 10000
  for i in range(inventory.NUM_OF_MACHINES):
    inventory.getWorker('127.0.0.1:{0}'.format(BASE_PORT+1+i))
  inventory.toJson(path)

  pid = fork_processes(inventory.NUM_OF_MACHINES, max_restarts=0)
  app = tornado.web.Application(([(r"/train?", offline.TrainingHandler)]))
  port = BASE_PORT+1+pid
  #app.setInventory(path)
  app.listen(port)
  print 'A classification worker is working at ' + inventory.MACHINES_IN_USE[pid]
  tornado.ioloop.IOLoop.instance().start()

	

	





	
