import json

NUM_OF_MACHINES = 5
MACHINES_IN_USE = []

def getWorker(address):
	if len(MACHINES_IN_USE) < NUM_OF_MACHINES:
		MACHINES_IN_USE.append(address)
		return True
	else:
		return False

def releaseWorker(address):
	if address in MACHINES_IN_USE:
		MACHINES_IN_USE.remove(address)
		return True
	else:
		return False

def toJson(path):
	f = open(path, "w")
	f.write(json.dumps(MACHINES_IN_USE))
	f.close()
	print 'Machines\' info has been written to \"'+path + '\"'  




