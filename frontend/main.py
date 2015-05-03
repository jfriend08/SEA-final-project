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

backend = backendInfo.BackendInfo('config/worker_info.json')

nClassifier = len(backend.info['classifier'])
curClassifier = 0
nSearch = len(backend.info['search'])
curSearch = 0
nRecommand = len(backend.info['recommand'])
curRecommand = 0

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
    return 'http://'+worker+'/predict?'+s
  def formSearchUrl(self, q, g):
    global curSearch
    worker = backend.info['search'][curSearch]
    curSearch += 1
    if curSearch == nSearch: curSearch = 0
    query = {}
    query['query'] = q
    query['genre'] = g
    s = urllib.urlencode(query)
    #print urllib.unquote(s)
    return 'http://'+worker+'/search?'+s
  def formRecommandUrl(self, u, g):
    global curRecommand
    worker = backend.info['recommand'][curRecommand]
    curRecommand += 1
    if curRecommand == nRecommand: curRecommand = 0
    query = {}
    query['user'] = u
    query['genre'] = g
    s = urllib.urlencode(query)
    return 'http://'+worker+'/recommand?'+s
  def get(self):
    query = self.request.get('q')
    genres = []
    if query:
      url = self.formClassifierUrl(query)
      self.response.write(url+'<br>')
      result = urlfetch.fetch(url)
      scores = json.loads(result.content)['scores']
      #self.response.write(str(scores)+'<br>')
      for pair in scores:
        if pair[1] >= 0.7:
          genres.append(str(pair[0]))
      self.response.write(str(genres)+'<br>')
      url = self.formSearchUrl(query, genres)
      self.response.write(url+'<br>')
    
    user = users.get_current_user()
    if user:
      url = self.formRecommandUrl(user.user_id(), genres)
      self.response.write(url+'<br>')
      link = users.create_logout_url('/')
    else:
      link = users.create_login_url('/')
    template_values = {'user': user, 'link': link , 'query': query}
    template = JINJA_ENVIRONMENT.get_template('template/search.html')
    self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
  ('/', MainHandler)
], debug=True)