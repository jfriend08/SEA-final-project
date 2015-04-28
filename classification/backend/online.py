import tornado.web
from tornado import gen
import pickle
import string
import json

class Application(tornado.web.Application):
  def setGenres(self, picklePath):
    self.genres = pickle.load(open(picklePath, "r"))
  def setWeights(self, picklePath):
    self.weights = pickle.load(open(picklePath, "r"))

# http://127.0.0.1:15001/predict?description=celia&threshold=0.8
class PredictionHandler(tornado.web.RequestHandler):
  @gen.coroutine
  def get(self):
    description = self.get_arguments('description')[0]
    threshold = float(self.get_arguments('threshold')[0])
    # trim the data
    s = str(description)
    s = s.translate(string.maketrans("",""), string.punctuation)
    s = s.lower()
    words = s.strip().split()
    # initialize the scores
    scores = []
    for i in range(len(self.application.genres)):
      scores.append(0.0)
    # update scores
    for w in words:
      if w in self.application.weights:
        temp = self.application.weights[w]
        for i in range(len(self.application.genres)):
				  scores[i] += temp[i]
      else:
        for i in range(len(self.application.genres)):
          scores[i] += 0.5
    res = []
    for i in range(len(scores)):
      scores[i] /= len(words)
      if scores[i] > threshold:
        res.append(self.application.genres[i])
    print scores
    res = {"status": "success", "possible_genre": res }
    self.write(json.dumps(res))
