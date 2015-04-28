# tornado
from tornado.process import fork_processes
import tornado.ioloop
import tornado.web
# package
from config import inventory
from backend import online
# 
import sys
import argparse

def getArguments(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument('numServer', type=int, default=inventory.NUM_OF_MACHINES, nargs='?', metavar='<NUM_OF_SERVER>', help='The number of working servers')
  parser.add_argument('outputPath', default='classification_server_address.json', nargs='?', metavar='<PATH_TO_SERVER_ADDRESSES>', help='path to the server address file')
  parser.add_argument('--genresPath', required=True, metavar='<PATH_TO_PICKLED_GENRE_LIST>', help='pickle file of the genres list')
  parser.add_argument('--weightsPath', required=True, metavar='<PATH_TO_PICKLED_GENRE_WEIGHTS_DICT>', help='pickle file of the weights dict')
  return parser.parse_args(argv)

# python -m classification.servers --genresPath constants/classification_weights/genres.p --weightsPath constants/classification_weights/big_weight.p 3 classification/server_address.json
if __name__ == "__main__":
  args = getArguments(sys.argv[1:])
  if args.numServer > inventory.NUM_OF_MACHINES: args.numServer = inventory.NUM_OF_MACHINES
  
  BASE_PORT = 15000
  for i in range(args.numServer):
    inventory.getWorker('127.0.0.1:{0}'.format(BASE_PORT+1+i))
  inventory.toJson(args.outputPath)

  pid = fork_processes(args.numServer, max_restarts=0)
  app = online.Application(([(r"/predict?", online.PredictionHandler)]))
  port = BASE_PORT+1+pid
  app.setGenres(args.genresPath)
  app.setWeights(args.weightsPath)
  app.listen(port)
  print 'A classification server is serving at ' + inventory.MACHINES_IN_USE[pid]
  tornado.ioloop.IOLoop.instance().start()

	

	





	
