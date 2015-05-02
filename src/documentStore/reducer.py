import sys
import pickle
from mapreduce.config import settings
indexer = {}
for line in sys.stdin:
  #separate key and value
  kvPair = line.split(settings.delimiter, 1)
  docid = kvPair[0]
  content = eval(kvPair[1])
  indexer[docid] = content  
#print pickle.dumps(indexer)
print indexer

