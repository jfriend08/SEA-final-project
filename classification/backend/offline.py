# tornado 
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
# 
import json
import pickle

# {u'movie_name1':{type:action, desciption:xxx}, movie_name2:{}, ...}
trainingSet = []
# {word1:0.51, word2:0.38, ...}
weight = {}
temp = {}
# [action, comedy, ...]
genre = set([])

class TrainingHandler(tornado.web.RequestHandler):
  accuracy = 0.0
  adjust = 0.01
  @gen.coroutine
  def get(self):
    picklePath = self.get_arguments('picklePath')[0]
    self.setTrainingSet(picklePath)
    print '===== reset training set ==========='

		# g(genre): train to recognize if the movie is that genre or not
    g = self.get_arguments('genre')[0]
    if g not in genre or len(trainingSet)==0:
      res = {"status": "failed", "info": 'genre not supported or no trainingSet'}
      #res = {"status": "failed", "info": g}
      self.write(json.dumps(res))
      return                
		# required accuracy
    require = float(self.get_arguments('requireAccuracy')[0])
		# maximum try times
    maxtry = int(self.get_arguments('maxTry')[0])
    # adjust amount if incorrect
    self.adjust = float(self.get_arguments('adjustAmount')[0])
    # to reset the training set
    picklePath = self.get_arguments('picklePath')[0]
    print '===== got necessary parameters ====='

    count = 0
    while self.accuracy < require:
      if count == maxtry:
        res = {"status": "failed", "info": 'couldn\'t reach accuracy in '+str(maxtry)+' rounds', 'accuracy': str(self.accuracy) }
        self.write(json.dumps(res))
        print 'failed'
        return
      global weight 
      weight = dict(temp)
      self.train(g)
      count += 1
      print str(count)+' ===== accuracy: '+str(self.accuracy)
    res = {"status": "success", "weight": weight}
    self.write(json.dumps(res))
    print 'success'

  def setTrainingSet(self, picklePath):
    global trainingSet
    global temp
    temp = {}
    trainingSet = pickle.load(open(picklePath, "r"))
    count = 0
    for movie in trainingSet:
      for g in movie['genres']: 
        genre.add(g)
      words = movie['synopsis'].strip().split()
      for w in words:
        if w not in temp:
          temp[w] = 0.5
      count += 1

  def train(self, g):
    global weight, trainingSet
    correct = 0
    for movie in trainingSet:
      words = movie['synopsis'].strip().split()
      score = 0.0
      for w in words:
        score += weight[w]
      #print score/len(words)
			# positive
      if score/len(words) >= 0.8:
        if g in movie['genres']:
          correct += 1
        else:
          self.adjustWeight(words, 'down')
      elif score/len(words) >= 0.2:
        if g in movie['genres']:
          self.adjustWeight(words, 'up')
        else:
          self.adjustWeight(words, 'down')
      # negative
      else:
        if g not in movie['genres']:
          correct += 1
        else:
          self.adjustWeight(words, 'up')
    self.accuracy = float(correct)/len(trainingSet)
	
  def adjustWeight(self, words, move):
    #print '============ adjust: '+move
    global temp
    if move == 'up':
      change = self.adjust
    else:
      change = -self.adjust
    for w in words:
      #temp[w] *= 1+change
      temp[w] += change
      #if temp[w] > 1: temp[w] = 1



