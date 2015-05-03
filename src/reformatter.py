import pickle
import os
from mapreduce.config import settings
import sys
"""

This module takes input:
  'constants/Review_dict',
  'constants/Genre_dict',
and splits them into sys.argv[1] sys.argv[2].in files in:
  'constants/input_review/'
  'constants/input_movie/'

"""
def reformat(input_path, output_path, num):
  # load all data into @data
  data = pickle.loads(open(input_path).read())
  # split data into @num partitions in @files
  files = {}
  print '---------- splitting %s data ----------' % input_path
  for key in data:
    line = key + settings.delimiter + str(data[key])
    try:
      files[hash(key)%num].append(line)
    except:
      files[hash(key)%num] = [line]
  #check if directory exists 
  if not os.path.exists(output_path):
    os.makedirs(output_path)
  print '---------- splitting successful ----------'

  #dump
  print '---------- dumping data to %s ----------' % output_path
  for i in xrange(num):
    path = '%s/%s.in' % (output_path, i) 
    f = open(path, 'w')
    print '           storing to %s           ' % path
    f.write('\n'.join(files[i]))
    f.close()
  print '---------- finished ----------'
  
if __name__ == "__main__":
  reformat('constants/Review_dict', 'constants/input_review', int(sys.argv[1]))
  reformat('constants/Genre_dict', 'constants/input_movie', int(sys.argv[2]))

