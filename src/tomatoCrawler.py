import tornado.httpserver
import tornado.ioloop
import tornado.web
import hashlib
import socket
import getpass
import urllib,re, zlib,time
import pickle
import json

from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPClient
from tornado import gen
from tornado.options import define, options

####################################################
#
# This module extracts movie IDs and Reviews from RottonTomato:
# Usage:
# python tomatoCrawler.py   then will save Movie_dict and Review_dict as pickle files
# 
# Review_dict[movieIDs].keys() --> [u'ratings', u'links', u'title', u'critics_consensus', u'release_dates', u'abridged_cast', u'synopsis', u'mpaa_rating', u'year', u'alternate_ids', u'posters', u'runtime', u'id']
# Review_dict[movieIDs].keys() --> [u'reviews', u'total', u'link_template', u'links']
#
####################################################


## Some constant info
import movieNameInventory as Inv 
import constantModule as CM
Movies = Inv.getMovieNames()
IDs = [] # collect return ids. Note: will be more than Movies list (e.g. will get two returns for divergent)
Movie_dict = {} # key is movie ID, value is a dict of the movie search return
Review_dict = {} # key is the movie ID



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
    toFetch = CM.MovieSearch(movie)
    print bcolors.OKGREEN + "Fetching: " + toFetch + bcolors.ENDC
    data = _load_json_from_url(toFetch)   
    
    for i in range(data['total']):
      try:
        IDs.append(data['movies'][i]['id'])
        Movie_dict[data['movies'][i]['id']] = data['movies'][i]
      except:
        pass
    time.sleep(0.5) #tomato server will not happy if you fetch too fast

@gen.coroutine
def tomatoReviewSeach():
  global Movies, IDs, Movie_dict, Review_dict 
  
  for myid in IDs:
    pageNum=1
    toFetch = CM.ReviewSearch(myid,pageNum)   
    data = _load_json_from_url(toFetch)   
    time.sleep(1)   
    print bcolors.OKGREEN + "MovieID:\t%s\tTitle:\t%s\tTotal Reviews:\t%d" %(myid, Movie_dict[myid]['title'], data['total']) + bcolors.ENDC   
    
    #API only provide 50 reviews per page, so fetching more pages if total review is more than 50
    if(data['total']>50):
      loop = int((data['total']+49)/50)-1
      for i in range(loop):
        pageNum+=1        
        toFetch = CM.ReviewSearch(myid,pageNum)   
        new_data= _load_json_from_url(toFetch)
        data['reviews'].extend(new_data['reviews'])               
        time.sleep(0.5) #tomato server will not happy if you fetch too fast
    
    Review_dict[myid] = data
        
    
    


if __name__ == "__main__":        
  import color
  bcolors = color.bcolors()

  print bcolors.HEADER + "====== START: tomatoMovieSearch ======" + bcolors.ENDC
  tornado.ioloop.IOLoop.current().run_sync(tomatoMovieSearch)
  print bcolors.OKBLUE + "Number of IDs: " +  str(len(IDs)) + bcolors.ENDC  

  # for myid in IDs:
  #   print "myid: " + myid     
  # for key in Movie_dict.keys():
  #   print str(key) + "\t" + Movie_dict[key]['title'] + "\n" + Movie_dict[key]['synopsis']
  
  print bcolors.HEADER + "====== START: tomatoReviewSeach ======" + bcolors.ENDC
  tornado.ioloop.IOLoop.current().run_sync(tomatoReviewSeach)
  # for key in Review_dict.keys():
  #   print str(key) + "\t" + Movie_dict[key]['title'] + "\n" + str(len(Review_dict[key]['reviews'])) 

  print bcolors.HEADER + "====== Saving PICKLE ======" + bcolors.ENDC
  fileObj = open('../constants/Movie_dict', 'w')
  pickle.dump(Movie_dict, fileObj)
  fileObj.close()    

  fileObj = open('../constants/Review_dict', 'w')
  pickle.dump(Review_dict, fileObj)
  fileObj.close()    


  print bcolors.OKGREEN + "Keys in Movie_dict[MovieID]\n" + bcolors.ENDC + str(Movie_dict[Movie_dict.keys()[0]].keys())
  print bcolors.OKGREEN + "Keys in Review_dict[MovieID]\n" + bcolors.ENDC + str(Review_dict[Review_dict.keys()[0]].keys())
  

