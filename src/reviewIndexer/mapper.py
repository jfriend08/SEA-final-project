import sys
from mapreduce.config import settings
for line in sys.stdin:
  kvPair = line.split(settings.delimiter, 1)
  movieId = kvPair[0]
  value = eval(kvPair[1])
  for review in value['reviews']:
    try:
      reviewer = review['critic']
      rating = review['original_score']
      print reviewer + settings.delimiter + str((movieId, rating))
    except:
      pass


