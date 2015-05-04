# tornado
from tornado.process import fork_processes
import tornado.ioloop
import tornado.web
# package
from classification.config import inventory
from classification.backend import offline
from mapreduce.backend import map, reduce, application
# 
import sys
import argparse

def getArguments(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument('nClassificationWorker', default=5, metavar='<PATH_TO_MAPPER>', help='Input file name')
  parser.add_argument('nMapreduceWorker', default=5, metavar='<PATH_TO_REDUCER>', help='Input file name')
  parser.add_argument('--jsonPath', default='prework_workers.json',metavar='<PATH_TO_JOB_DIR>', help='Input file name')
  parser.add_argument('--startPort', default=10000,metavar='<PATH_TO_JOB_DIR>', help='Input file name')
  return parser.parse_args(argv)

if __name__ == "__main__":
  args = getArguments(sys.argv[1:])
  print args.nMapreduceWorker
  print args.nClassificationWorker
  print args.jsonPath
  print args.startPort

  '''
  BASE_PORT = 20000
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
  '''
	





	
