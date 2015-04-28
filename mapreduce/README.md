# MapReduce Framework

## write mapper/reducer

Besure to use the preset delimiter

```python

from mapreduce.config import settings
...
print settings.delimiter.join([key, term, str(tracker[key][term])])

```

## initialize workers

run the script and it will generate a .json file containing the workers' ip addresses

```
$ python -m mapreduce.workers
```

## run your mapper/reducer jobs via the framework

getWorkerInfo() takes one argument: 
the path to the result json file of executing workers.py

```python

import mapreduce.framework as framework
import tornado.ioloop

mrf = framework.MapReduceFramework()
mrf.getWorkerInfo('address.json')
mrf.mapReduce('invertedIndex/ii_jobs', 'invertedIndex.IImapper', 4, 'invertedIndex.IIreducer', 'constants/invertedIndex')
tornado.ioloop.IOLoop.instance().start()
 
```

mapReduce() takes four arguments:

1. inputDir: path to your input files
2. mapperPath: path to your mapper (module)
3. nReducers: to specify the number of output files
4. reducerPath: path to your reducer (module)
5. outputDir: path to your output files

```python

def mapReduce(self, inputDir, mapperPath, nReducers, reducerPath, outputDir):

```
and it printout following information along the way

1. input file names
2. number of taskIDs
3. url request to recuders
4. reducer's feedbacks
5. finish notice


