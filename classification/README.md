# Query Classification

## initialize workers

```
$ python -m classification.workers <PATH_TO_WORKER_ADDRESS_JSON>
$ python -m classification.workers classification/worker_address.json

```

## training

```python

import classification.trainer as trainer

# path variables
worker_address = 'classification/worker_address.json'
raw_data = 'constants/Genre_dict'
training_set = 'constants/training_set.p'
weights_dir = 'constants/classification_weights'

# constructor
tn = trainer.Trainer()

# tell the trainer where are its workers
tn.setWorkerInfo(worker_address)

# process raw data and get all possible genres
# def processRawData(self, inputPath, outputPath):
genres = tn.processRawData(raw_data, training_set)

# set training parameters 
# def setTraningParameter(self, accuracy_requirement, max_try, adjust_amount_each):
tn.setTraningParameter(0.9, 200, 0.01)

# training
# def train(self, trainingSetPath, possible_genres, outputDir):
tn.train(training_set, genres, weights_dir)
tornado.ioloop.IOLoop.instance().start()

# combine the training results
# def generateWeightTable(self, weightsDir):
tn.generateWeightTable(weights_dir)

```

## run the servers

usage: servers.py [-h] --genresPath <PATH_TO_PICKLED_GENRE_LIST> --weightsPath <PATH_TO_PICKLED_GENRE_WEIGHTS_DICT> \[<NUM_OF_SERVER>\] \[<PATH_TO_SERVER_ADDRESSES>\]

```
$ python -m classification.servers --genresPath constants/classification_weights/genres.p --weightsPath constants/classification_weights/big_weight.p 3 classification/server_address.json

```

## test

```
$ curl "http://127.0.0.1:15001/predict?description=celia&threshold=0.8"

```

