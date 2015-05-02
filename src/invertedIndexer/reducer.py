import sys
import pickle
from mapreduce.config import settings
indexer = {}
inverted_dic = {}
pre_word = None
count = 0
for line in sys.stdin:
  #separate key and value
  kvPair = line.split(settings.delimiter, 1)
  word = kvPair[0]
  docid = eval(kvPair[1])
  
  if pre_word and word != pre_word:
    indexer[pre_word] = inverted_dic
    inverted_dic = {}
  try:
    inverted_dic[docid] += 1
  except:
    inverted_dic[docid] = 1
  pre_word = word
print pickle.dumps(indexer)

