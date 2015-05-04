# tornado
from tornado.process import fork_processes
import tornado.ioloop
import tornado.web
# package
from config import inventory
from backend import map, reduce, application

if __name__ == "__main__":

  BASE_PORT = 20000
  path = 'mapreduce_workers.json'
  for i in range(inventory.NUM_OF_MACHINES):
    inventory.getWorker('127.0.0.1:{0}'.format(BASE_PORT+1+i))
  inventory.toJson(path)

  pid = fork_processes(inventory.NUM_OF_MACHINES, max_restarts=0)
  app = application.Application(([(r"/map?", map.MapHandler),
                                  (r"/retrieveMapOutput?", map.RetrieveOutputHandler),
                                  (r"/reduce?", reduce.ReduceHandler),
                                  ]))
  port = BASE_PORT+1+pid
  app.setInventory(path)
  app.listen(port)
  print 'A worker is working at ' + inventory.MACHINES_IN_USE[pid]
  tornado.ioloop.IOLoop.instance().start()

	

	





	
