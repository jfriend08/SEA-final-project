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
    print "description%s" % description
    #threshold = float(self.get_arguments('threshold')[0])
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
    res1 = []
    #res2 = []
    for i in range(len(scores)):
      scores[i] /= len(words)
      res1.append((self.application.genres[i], scores[i]))
      #if scores[i] > threshold: res2.append(self.application.genres[i])
    #sorted(student_tuples, key=lambda student: student[2])
    res1 = sorted(res1, key=lambda x:x[1], reverse=True)
    print '===== PREDICT: '+s+' ====='
    print res1
    res = {"status": "success", "scores": res1 }
    #res = {"status": "success", "possible_genres": res2 }
    self.write(json.dumps(res))
