import mapreduce.framework as framework
import tornado.ioloop

mrf = framework.MapReduceFramework()
mrf.getWorkerInfo('address.json')
mrf.mapReduce('invertedIndex/ii_jobs', 'invertedIndex.IImapper', 4, 'invertedIndex.IIreducer')
tornado.ioloop.IOLoop.instance().start()
