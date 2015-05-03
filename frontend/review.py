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

nRater = len(backend.info['rate'])
curRater = 0

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ReviewHandler(webapp2.RequestHandler):
  def formRateUrl(self, uid, mid, rate):
    global curRater
    worker = backend.info['rate'][curRater]
    curRater += 1
    if curRater == nRater: curRater = 0
    query = {}
    query['uid'] = uid
    query['mid'] = mid
    query['rate'] = rate
    s = urllib.urlencode(query)
    return 'http://'+worker+'/recommand?'+s
  def post(self):
    mid = self.request.get('mid')
    rate = self.request.get('rate')
    title = self.request.get('title')
    user = users.get_current_user()
    link = users.create_logout_url('/')
    if rate:
      url = self.formRateUrl(user.user_id(), mid, rate)
      #response = urlfetch.fetch(url)
      #result = json.loads(response.content)
      self.redirect("/")
    template_values = {'user': user, 'link': link , 'mid': mid, 'title': title}
    template = JINJA_ENVIRONMENT.get_template('template/review.html')
    self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
  ('/review', ReviewHandler)
], debug=True)