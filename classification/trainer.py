# 
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
#
import pickle
import json
import urllib
import os
import string

class Trainer:
  workers = []
  nMachines = 0
  accuracy = 0.9
  maxtry = 200
  adjust = 0.01

  def setWorkerInfo(self, jsonPath):
    self.workers = json.load(open(jsonPath, "r"))
    self.nMachines = len(self.workers)
    print self.workers

  def processRawData(self, inputPath, outputPath):
    raw = pickle.load(open(inputPath, "r"))
    data = []
    genres = set([])
    count = 0
    for key in raw.keys():
      movie = raw[key]
      # if no genre or synopsis data
      if 'genres' not in movie or 'synopsis' not in movie: continue
      if len(movie['genres'])==0 or movie['synopsis'] == '': continue
      temp = {}
      temp['genres'] = movie['genres']
      for g in temp['genres']:
        genres.add(g)
      # trim out the punctuation and transform to lowercase
      s = str(movie['synopsis'])
      s = s.translate(string.maketrans("",""), string.punctuation)
      temp['synopsis'] = s.lower()
      data.append(temp)
      count += 1
    # output as a pickle file 
    file = open(outputPath, 'wb')
    pickle.dump(data, file)
    print 'processed ' + str(count) + ' movies'
    return genres

  def setTraningParameter(self, accuracy, maxtry, adjust):
    self.accuracy = accuracy
    self.maxtry = maxtry
    self.adjust = adjust

  @gen.coroutine
  def train(self, setPath, genres, outputDir):
    print '====== start training ====='
    if not os.path.exists(outputDir): os.mkdir(outputDir)
    genres = list(genres)
    idx = 0
    num = 0
    while num < len(genres):
      g = genres[num]
      w = self.workers[idx%self.nMachines]
      url = self.formTrainQuery(w, g, setPath)
      print url
      http_client = AsyncHTTPClient()
      response = yield http_client.fetch(url)
      temp = json.loads(response.body)
      if temp['status'] == 'success':
        print '=========== success on '+g
        file = open(str(outputDir)+'/'+str(g)+'.out', 'w')
        pickle.dump(temp['weight'], file)
        # json.dump(temp['weight'], file)
        file.close()
      else:
        print temp
      num += 1
      idx += 1

    print '========== DONE '
    tornado.ioloop.IOLoop.current().stop()

  def formTrainQuery(self, worker, genre, setPath):
    query = {}
    query['genre'] = genre
    query['requireAccuracy'] = str(self.accuracy)
    query['maxTry'] = str(self.maxtry)   
    query['adjustAmount'] = str(self.adjust)
    query['picklePath'] = setPath
    s = urllib.urlencode(query)
    return 'http://'+worker+'/train?'+s

  def generateWeightTable(self, weightsDir):
    bigWeight = {}
    genres = []
    # gather small weight files
    weightFiles = []
    for f in os.listdir(weightsDir):
      if '.out' in f:
        weightFiles.append(weightsDir+'/'+f)
        genres.append(f.replace('.out',''))
    if len(weightFiles)==0: return
    # initiate bigWeight
    temp = pickle.load(open(weightFiles[0], "r"))
    for key in temp.keys():
      bigWeight[key] = [];
    # fill in the weights 
    for f in weightFiles:
      temp = pickle.load(open(f, "r"))
      for key in temp.keys():
        bigWeight[key].append(temp[key])
    # output as pickle
    path = weightsDir+'/genres.p' 
    file = open(path, 'w')
    pickle.dump(genres, file)
    file.close()
    print 'Write genres to '+path
    #
    path = weightsDir+'/big_weight.p'
    file = open(weightsDir+'/big_weight.p', 'w')
    pickle.dump(bigWeight, file)
    file.close()
    print 'Write bigWeight to '+path




