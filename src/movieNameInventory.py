from tornado import ioloop, web, gen, httpclient
from tornado.ioloop import IOLoop
import json
import re

####################################################
#
# This module extracts movie names from website:
# http://www.imdb.com/chart/top?ref_=nv_ch_250_4
# 
# Usage:
# getMovieNames() will return a list of movies names
#
####################################################
@gen.coroutine
def readHtml():
  http = httpclient.AsyncHTTPClient()
  response = yield http.fetch(url)
  global body
  body = response.body

def getMovieNames():
  global url
  url = 'http://www.imdb.com/chart/top?ref_=nv_ch_250_4'
  IOLoop.current().run_sync(readHtml)
  match = re.findall('.*title=".[^"]*" >(.[^<]*)</a>',body)[1:]
  return match

if __name__ == "__main__":
  print getMovieNames()
