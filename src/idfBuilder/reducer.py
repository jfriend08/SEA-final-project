import sys
import pickle
import math
from mapreduce.config import settings
indexer = {}
inverted_dic = {}
pre_word = None
count = 0
docs = {}
for line in sys.stdin:
  #separate key and value
  kvPair = line.split(settings.delimiter, 1)
  word = kvPair[0]
  docid = eval(kvPair[1])

  #calculate # of docs
  docs[docid] = 1
  
  #calculate document frequency
  if pre_word and word != pre_word:
    indexer[pre_word] = inverted_dic
    inverted_dic = {}
  inverted_dic[docid] = 1
  pre_word = word

#calculate idf
N = len(docs) 
idf = {}
for term in indexer:
  idf[term] = math.log(N / float(len(indexer[term])))
print pickle.dumps(idf)

