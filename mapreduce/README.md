# MapReduce Framework

## write mapper/reducer

Besure to use the preset delimiter

```python

import mapreduce.config.settings as settings

for key in tracker.keys():
	for term in tracker[key].keys():
		print settings.delimiter.join([key, term, str(tracker[key][term])])

```

## initialize workers

run the script and you will get a .json containing the workers' ip addresses

```
$ python mapreduce/workers.py

```

## run your mapper/reducer jobs via the framework


```python

import mapreduce.framework as framework
import tornado.ioloop

mrf = framework.MapReduceFramework()
mrf.getWorkerInfo('address.json')
mrf.mapReduce('invertedIndex/ii_jobs', 'invertedIndex/IImapper.py', 4, 'invertedIndex/IIreducer.py')
tornado.ioloop.IOLoop.instance().start()
 
```

getWorkerInfo() takes one argument: 
the path to the result json file of executing workers.py

mapReduce() takes four arguments:

1. jobPath: path to your input files
2. mapperPath: path to your mapper
3. nReducers: to specify the number of output files
4. reducerPath: path to your reducer

```python
def mapReduce(self, jobPath, mapperPath, nReducers, reducerPath):

```
and it printout 
1. input file names
2. number of taskIDs
3. url request to recuders
4. reducer's feedbacks
5. finish notice


