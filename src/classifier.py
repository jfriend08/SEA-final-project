# tornado 
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
# 
import json

# {u'movie_name1':{type:action, desciption:xxx}, movie_name2:{}, ...}
trainingSet = {}
# {word1:0.51, word2:0.38, ...}
weight = {}
temp = {}
# [action, comedy, ...]
genre = set([])

# http://127.0.0.1:8080/predict?
class PredictionHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
        if len(weight)==0:
            res = {"status": "failed", "info": 'no weight info'}
        else:
            desciption = self.get_arguments('desciption')[0]
            words = desciption.strip().split('+')
            score = 0
            for w in words:
                score += weight[w]
            res = {"status": "success", "score": score/len(words) }
        self.write(json.dumps(res))

class TrainingSetHandler(tornado.web.RequestHandler):
	@gen.coroutine
	def get(self):
		# inputs: training set file path and num of movies
		jsonPath = self.get_arguments('jsonPath')[0]
		numMovies = int(self.get_arguments('numMovies')[0])
		# 
		trainingSet = json.load(open(jsonPath, "r"))
		count = 0
		for movie in trainingSet:
			genre.add(movie['type'])
			words = movie['desciption'].strip().split()
			for w in words:
				if w not in weight:
					temp[w] = 0.5
			count += 1
		#
		if count==numMovies: res = {"status": "success", "processed": count}
		else: res = {"status": "failed", "processed": count}
		self.write(json.dumps(res))

class ClassificationHandler(tornado.web.RequestHandler):
	accuracy = 0.0
	adjust = 0.01
	@gen.coroutine
	def get(self):
		# g(genre): train to recognize if the movie is that genre or not
		g = self.get_arguments('genre')[0]
		if g not in genre or len(trainingSet)==0:
			res = {"status": "failed", "info": 'genre not supported or no trainingSet'}
			self.write(json.dumps(res))
			return                
		# required accuracy
		require = float(self.get_arguments('requireAccuracy')[0])
		# maximum try times
		maxtry = int(self.get_arguments('maxTry')[0])
		# adjust amount if incorrect
		self.adjust = float(self.get_arguments('adjustAmount')[0])
		count = 0

		while self.accuracy < require:
			if count == maxtry:
				res = {"status": "failed", "info": 'couldn\'t reach accuracy in '+str(maxtry)+' rounds' }
				self.write(json.dumps(res))
				return
			weight = temp
			self.train(g)
			count += 1
		res = {"status": "success", "accuracy": accuracy}
		self.write(json.dumps(res))

	def train(self, g):
		correct = 0
		for movie in trainingSet:
			words = movie['desciption'].strip().split()
			score = 0
			for w in words:
				score += weight[w]
			# correctly positive
			if score/len(words) > 0.5 and movie['type']==g:
				correct += 1
			# correctly negative
			elif score/len(words) < 0.5 and movie['type']!=g:
				correct += 1
			# incorrectly negative
			elif score/len(words) < 0.5 and movie['type']==g:
				adjustWeight(words, 'up')
			# incorrectly positive
			elif score/len(words) > 0.5 and movie['type']!=g:
				adjustWeight(words, 'down')
		self.accuracy = float(correct)/len(trainingSet)
	
	def adjustWeight(self, words, move):
		if move == 'up':
			change = self.adjust
		else:
			change = -self.adjust
		for w in words:
			temp[w] *= 1+change


if __name__ == "__main__": 
	app = tornado.web.Application(([(r"/predict?", PredictionHandler),
                                    (r"/trainingSet?", TrainingSetHandler)
                                    (r"/train?", ClassificationHandler)
                                    ]))
    app.listen(8080)
    print 'listening to port 8080...'
    tornado.ioloop.IOLoop.instance().start()


