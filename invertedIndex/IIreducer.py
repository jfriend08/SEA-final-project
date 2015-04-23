#!/usr/bin/env python

from itertools import groupby, imap
from operator import itemgetter
import sys
import pickle
import mapreduce.config.settings as settings

invertedIndexes = {}
data = imap(lambda x: x.strip().split(settings.delimiter), sys.stdin)
for did, term, fre in data:
  if term not in invertedIndexes:
    invertedIndexes[term] = []
  invertedIndexes[term].append((int(did), fre))

print pickle.dumps(invertedIndexes)