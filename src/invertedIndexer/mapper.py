import sys
from mapreduce.config import settings
from nltk.tokenize import RegexpTokenizer
for line in sys.stdin:
  #separate key and value pair
  kvPair = line.split(settings.delimiter, 1)
  key = kvPair[0]
  value = eval(kvPair[1])
  for key in value:
    print key
  break
  """
  for review in value['reviews']:
    try:
      title = review['title']
      quote = review['quote']
      rating = review['original_score']
      print key + settings.delimiter + str((reviewer, rating, quote))
    except:
      pass
  """

