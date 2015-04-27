from base import DisList, DisTable

from .constants import Inventory

INVENTORY = None
MASTER = None

def setMaster(host):
  global MASTER
  MASTER = host

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
