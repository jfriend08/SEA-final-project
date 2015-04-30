from base import DisList, DisTable
from handler import FSHandler
from master import FSMaster
from workers import FSWorker

from tornado.httpclient import HTTPClient, AsyncHTTPClient

from .constants import Inventory

INVENTORY = None

def setMaster(host, port):
  global INVENTORY

  if INVENTORY == None:
    INVENTORY = Inventory()
  INVENTORY.setMaster(host, port)

def addWorker(hostName, port):
  global INVENTORY

  if INVENTORY == None:
    INVENTORY = Inventory()
  INVENTORY.attachServer(hostName, port)
  
def delWorker(hostName, port):
  global INVENTORY

  INVENTORY.detachServer(hostName, port)
  if INVENTORY.numServers == 0:
    INVENTORY = None

def shutDown():
  if not INVENTORY == None:
    INVENTORY.clearInfo()

INVENTORY = Inventory()

