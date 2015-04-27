import pickle
import os
from mapreduce.config import settings
"""

This module takes input 'constants/Review_dict' and 
splits it into @num .in files in 'constants/input/'

"""
def reformat(num):
  # load all data into @data
  data = pickle.loads(open('constants/Review_dict').read())
  # split data into @num partitions in @files
  files = {}
  for key in data:
    line = key + settings.delimiter + str(data[key])
    try:
      files[hash(key)%num].append(line)
    except:
      files[hash(key)%num] = [line]
  #check if directory exists
  directory = 'constants/input'
  if not os.path.exists(directory):
    os.makedirs(directory)

  #dump
  for i in xrange(num):
    f = open('%s/%s.in' % (directory, i) , 'w')
    f.write('\n'.join(files[i]))
    f.close()

if __name__ == "__main__":
  reformat(3)
