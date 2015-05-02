import sys
from mapreduce.config import settings
from nltk.tokenize import RegexpTokenizer as RT
for line in sys.stdin:

  #separate key and value pair
  kvPair = line.split(settings.delimiter, 1)
  docid = kvPair[0]
  value = eval(kvPair[1])
  
  #get bag of words
  try:
    title = value['title']
  except:
    title = ''
  try:
    synopsis = value['synopsis']
  except:
    synopsis = ''
  #cast = value['abridges_cast']

  #parse
  tokenizer = RT(r'\w+')
  terms = tokenizer.tokenize(' %s %s %s ' % (synopsis, title, title) )

  #output
  for term in terms:
    print term + settings.delimiter + docid

