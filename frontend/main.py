#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import json
import urllib
from google.appengine.api import users
from google.appengine.api import urlfetch
from config import backendInfo
import urllib2
#from tornado.httpclient import AsyncHTTPClient

backend = backendInfo.BackendInfo('config/workers.json')

nClassifier = len(backend.info['classifier'])
curClassifier = 0
nSearch = len(backend.info['search'])
curSearch = 0
nRecommend = len(backend.info['recommend'])
curRecommend = 0

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
  def formClassifierUrl(self, q):
    global curClassifier
    worker = backend.info['classifier'][curClassifier]
    curClassifier += 1
    if curClassifier == nClassifier: curClassifier = 0
    query = {}
    query['description'] = q
    s = urllib.urlencode(query)
    #return 'http://'+worker+'/predict?'+s
    return worker+'/predict?'+s
  def formSearchUrl(self, q, g):
    global curSearch
    worker = backend.info['search'][curSearch]
    curSearch += 1
    if curSearch == nSearch: curSearch = 0
    query = {}
    query['q'] = q
    query['genre'] = g
    s = urllib.urlencode(query)
    #print urllib.unquote(s)
    #return 'http://'+worker+'/search?'+s
    return worker+'/search?'+s
  def formrecommendUrl(self, u, g):
    global curRecommend
    worker = backend.info['recommend'][curRecommend]
    curRecommend += 1
    if curRecommend == nRecommend: curRecommend = 0
    query = {}
    query['user'] = u
    query['genre'] = g
    s = urllib.urlencode(query)
    #return 'http://'+worker+'/recommend?'+s
    return worker+'/recom?'+s
  def get(self):
    query = self.request.get('q')
    genres = []
    if query:
      # deal with classifier
      url = self.formClassifierUrl(query)
      #self.response.write(url+'<br>')
      result = urlfetch.fetch(url)
      scores = json.loads(result.content)['scores']
      #self.response.write(str(scores)+'<br>')
      for pair in scores:
        if pair[1] >= 1.0:
          genres.append(str(pair[0]))
      #self.response.write(str(genres)+'<br>')
      # deal with search engine
      url = self.formSearchUrl(query, genres)
      #self.response.write(url+'<br>')
      result = urlfetch.fetch(url)
      j = json.loads(result.content)
      search_genre = j['GenreResult']
      search_normal = j['NormalResult']
      search_result = search_genre + search_normal

    
    user = users.get_current_user()
    if user:
      # deal with search engine
      link = users.create_logout_url('/')
      #url = self.formrecommendUrl(user.user_id(), genres)
      url = self.formrecommendUrl('7f2b697d-d53a-4301-86a8-7ff5750d01e9', genres)
      #self.response.write(url+'<br>')
      result = urlfetch.fetch(url)
      recom_genre = json.loads(result.content)['GenreResult']
      recom_normal = json.loads(result.content)['NormalResult']
      #print recom_normal

    else:
      link = users.create_login_url('/')
    template_values = {'user': user, 'link': link , 'query': query, 'search_result': search_result, 'recom_genre': recom_genre, 'recom_normal': recom_normal }
    template = JINJA_ENVIRONMENT.get_template('template/search.html')
    self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
  ('/', MainHandler)
], debug=True)