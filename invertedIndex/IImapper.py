#!/usr/bin/env python

import sys
from ..mapreduce.config import settings

tracker = {}
eop = True
did = 0
for line in sys.stdin:
  if eop:
    parts = line.strip().split(settings.delimiter)
    did = parts[0]
    tracker[did] = {}
    words = parts[1].strip().split()
    for word in words:
      tracker[did][word] = 5
    eop = False
  else:
    words = line.strip().split()
    if len(words) == 0:
      continue
    if words[0] == '>>EOP<<':
      eop = True
      continue
    for word in words:
      if word not in tracker[did]:
        tracker[did][word] = 1
      else:
        tracker[did][word] += 1

for key in tracker.keys():
  for term in tracker[key].keys():
    print settings.delimiter.join([key, term, str(tracker[key][term])])

