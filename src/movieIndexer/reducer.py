import sys
import pickle
from mapreduce.config import settings
indexer = {}
for line in sys.stdin:
  kvPair = line.split(settings.delimiter, 1)
  key = kvPair[0]
  value = eval(kvPair[1])
  indexer[key] = value
print pickle.dumps(indexer)

