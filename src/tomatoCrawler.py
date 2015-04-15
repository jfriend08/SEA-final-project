import tornado.httpserver
import tornado.ioloop
import tornado.web
import hashlib
import socket
import getpass
import urllib,re, zlib,time

import json

from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPClient
from tornado import gen
from tornado.options import define, options

## Some constant info
Movies = ["divergent", "toy story 2", "hunger game", "INTERSTELLAR"]
IDs = [] # collect return ids. Note: will be more than Movies list (e.g. will get two returns for divergent)
Movie_dict = {} # key is movie ID, value is a dict of the movie search return
Review_dict = {} # key is the movie ID
MovieSearch = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=x6usx7bn33cdn9vverg9f2v7&q="
ReviewSearch = "http://api.rottentomatoes.com/api/public/v1.0/movies/#ID HERE#/reviews.json?apikey=x6usx7bn33cdn9vverg9f2v7&review_type=all&page_limit=50"
# ReviewSearch = "http://api.rottentomatoes.com/api/public/v1.0/movies/771315918/reviews.json?apikey=x6usx7bn33cdn9vverg9f2v7&review_type=all&page_limit=50"

def _load_json_from_url(url):
  """
  A wrapper around the api call. The response might be gzipped,
  which this will abstract away. Returns a JSON-decoded dictionary.
  """
  response = urllib.urlopen(url).read()

  # the response might be gzip'd
  try:
    # explanation of magic number:
    # http://stackoverflow.com/a/2695466/474683
    response = zlib.decompress(response, 16+zlib.MAX_WBITS)
  except zlib.error:
    # if there's an error, it's probably not gzip'd
    pass

  return json.loads(response)

@gen.coroutine
def tomatoMovieSearch():
	global Movies, IDs, Movie_dict, Review_dict
	for movie in Movies:
		toFetch = MovieSearch + movie.replace(" ", "%20")
		http_client = AsyncHTTPClient()
		response = yield http_client.fetch(toFetch)
		data = eval(response.body)
		for i in range(data['total']):			
			IDs.append(data['movies'][i]['id'])
			Movie_dict[data['movies'][i]['id']] = data['movies'][i]


@gen.coroutine
def tomatoReviewSeach():
	global Movies, IDs, Movie_dict, Review_dict	
	
	for myid in IDs:
		pageNum=1
		toFetch = "http://api.rottentomatoes.com/api/public/v1.0/movies/%s/reviews.json?apikey=x6usx7bn33cdn9vverg9f2v7&page_limit=50&review_type=all&page=%s" %(myid,pageNum)
		print toFetch
		data = _load_json_from_url(toFetch)		
		time.sleep(1)		
		print "myid: " + str(myid) + "\t" + "total: " + str(data['total'])
		
		if(data['total']>50):
			loop = int((data['total']+49)/50)-1
			for i in range(loop):
				pageNum+=1
				toFetch = "http://api.rottentomatoes.com/api/public/v1.0/movies/%s/reviews.json?apikey=x6usx7bn33cdn9vverg9f2v7&page_limit=50&review_type=all&page=%s" %(myid,pageNum)				
				new_data= _load_json_from_url(toFetch)
				data['reviews'].extend(new_data['reviews'])				
				# print data.keys()				
				# print len(data['reviews'])
				time.sleep(0.5)		
		
		Review_dict[myid] = data
				
		
		


if __name__ == "__main__":        
	tornado.ioloop.IOLoop.current().run_sync(tomatoMovieSearch)
	
	for myid in IDs:
		print "myid: " + myid 		
	for key in Movie_dict.keys():
		print str(key) + "\t" + Movie_dict[key]['title'] + "\n" + Movie_dict[key]['synopsis']

	tornado.ioloop.IOLoop.current().run_sync(tomatoReviewSeach)

	for key in Review_dict.keys():
		print str(key) + "\t" + Movie_dict[key]['title'] + "\n" + str(len(Review_dict[key]['reviews']))


