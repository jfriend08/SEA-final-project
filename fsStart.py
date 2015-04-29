#! /usr/bin/env python

import socket

import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.process import fork_processes
from tornado.netutil import bind_sockets

from fs import FSHandler, FSMaster, FSWorker
import fs

if __name__ == '__main__':
  numWorkers = 3
  hostName = socket.gethostname()

  BASE_PORT = 27375
  fs.setMaster(hostName, BASE_PORT)
  for p in xrange(numWorkers):
    fs.addWorker(hostName, BASE_PORT + p + 1)

  print fs.INVENTORY

  uid = fork_processes(numWorkers+1)
  sockets = bind_sockets(BASE_PORT + uid)

  if uid == 0:
    process = FSMaster(fs.INVENTORY.getMaster(), fs.INVENTORY.getWorkers())
  else:
    process = FSWorker(fs.INVENTORY.getWorkers()[uid-1])

  app = tornado.web.Application([
    (r'/fs?', FSHandler, dict(processObj=process)),
  ])
  server = HTTPServer(app)
  server.add_sockets(sockets)

  try:
    tornado.ioloop.IOLoop.current().start()
  except:
    print 'Shutting Down...'
  finally:
    fs.shutDown()
