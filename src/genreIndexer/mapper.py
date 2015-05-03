import sys
from mapreduce.config import settings
for line in sys.stdin:
  kvPair = line.split(settings.delimiter, 1)
  key = kvPair[0]
  value = eval(kvPair[1])
  try:
    genres = value['genres']
  except:
    genres = []
  print key + settings.delimiter + str(genres)


