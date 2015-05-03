import mapreduce.framework as framework
import classification.trainer as trainer
import tornado.ioloop
from src import color


def main():

  C = color.bcolors()

  print C.HEADER + "=========== Instantiate MapReduceFramework ===========" + C.ENDC  
  mrf = framework.MapReduceFramework()
  mrf.getWorkerInfo('address.json')
  
  #print C.HEADER + "=========== Start Local Indexing ===========" + C.ENDC
  # localIndexer.ReviewIndexing()
  
  print C.HEADER + "=========== Start Indexing Movies ===========" + C.ENDC
  mrf.mapReduce('constants/input_movie', 'src.invertedIndexer.mapper', 7, 'src.invertedIndexer.reducer', 'constants/invertedIndex')
  #tornado.ioloop.IOLoop.current().run_sync(mrf.mapReduce('constants/input_movie', 'src.invertedIndexer.mapper', 7, 'src.invertedIndexer.reducer', 'constants/invertedIndex'))
  tornado.ioloop.IOLoop.instance().start()
  mrf.mapReduce('constants/input_movie', 'src.idfBuilder.mapper', 1, 'src.idfBuilder.reducer', 'constants/idf')
  tornado.ioloop.IOLoop.instance().start()
  mrf.mapReduce('constants/input_movie', 'src.documentStore.mapper', 1, 'src.documentStore.reducer', 'constants/documentStore')
  tornado.ioloop.IOLoop.instance().start()

  
  print C.HEADER + "=========== Start Indexing Reviews ===========" + C.ENDC
  mrf.mapReduce('constants/input_review', 'src.movieIndexer.mapper', 7, 'src.movieIndexer.reducer', 'constants/movieIndexer')
  tornado.ioloop.IOLoop.instance().start()
  mrf.mapReduce('constants/input_review', 'src.reviewIndexer.mapper', 1, 'src.reviewIndexer.reducer', 'constants/reviewIndexer')
  tornado.ioloop.IOLoop.instance().start()

  print C.HEADER + "=========== Start Classification Training ===========" + C.ENDC
  worker_address = 'classification/worker_address.json'
  raw_data = 'constants/Genre_dict'
  raw_data = 'constants/Genre_dictII_9500'
  training_set = 'constants/training_set.p'
  weights_dir = 'constants/classification_weights'
  tn = trainer.Trainer()
  tn.setWorkerInfo(worker_address)
  genres = tn.processRawData(raw_data, training_set)
  tn.setTraningParameter(0.9, 200, 0.01)
  tn.train(training_set, genres, weights_dir)
  tornado.ioloop.IOLoop.instance().start()
  tn.generateWeightTable(weights_dir)

if __name__ == "__main__":
  main()
