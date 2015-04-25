import tornado.httpserver
import tornado.ioloop
import tornado.web
import hashlib
import socket
import getpass
import urllib,re, zlib,time
import pickle
import json, sys

from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPClient
from tornado import gen
from tornado.options import define, options

Review_dict = {}
Movie_dict = {}

Movie_Index_book = {}
Review_Index_book = {}

Movie_Index = {}
Review_Index= {}

NumMovieServer = 3
NumReviewServer = 3




def loadPockle(path):  
  mydict = pickle.load(open(path, 'r'))  
  return mydict 

def getInit():
  global NumMovieServer, NumReviewServer, Movie_Index_book, Review_Index_book
  for i in xrange(NumMovieServer):
    Movie_Index_book[i] = {}
  for i in xrange(NumReviewServer):
    Review_Index_book[i] = {}

def ParseGetMovie_Index(Review_dict):
  global NumMovieServer, NumReviewServer, Movie_Index_book, Review_Index_book
  for MovieID in Review_dict.keys():    
    book_idx = int(MovieID) % NumMovieServer
    Movie_Index_book[book_idx][MovieID] = []
    for eachReview in Review_dict[MovieID]["reviews"]:            
      try: 
        Movie_Index_book[book_idx][MovieID].append((eachReview["critic"], eachReview["original_score"]))
      except:
        pass
  return Movie_Index_book

def ParseGetReview_Index(Review_dict):
  global NumMovieServer, NumReviewServer, Movie_Index_book, Review_Index_book
  
  #Get init
  for MovieID in Review_dict.keys():
    for eachReview in Review_dict[MovieID]["reviews"]:
      criticName = eachReview['critic']
      book_idx = hash(criticName) % NumReviewServer
      Review_Index_book[book_idx][criticName] = []

  for MovieID in Review_dict.keys():
    for eachReview in Review_dict[MovieID]["reviews"]:
      criticName = eachReview['critic']
      book_idx = hash(criticName) % NumReviewServer
      try:
        Review_Index_book[book_idx][criticName].append((MovieID, eachReview["original_score"]) )
      except:
        pass
  return Review_Index_book

def countAllKeysFromBook(book):
  count = 0
  for key in book.keys():
    count += len(book[key].keys())
  return count

def dumpPickle(book, path, prefix):
  global NumMovieServer, NumReviewServer, Movie_Index_book, Review_Index_book
  for book_idx in book.keys():
    filename = path + prefix + str(book_idx)    
    fileObj = open(filename, 'w')
    pickle.dump(book[book_idx], fileObj)    
    fileObj.close() 

def ReviewIndexing():
  global NumMovieServer, NumReviewServer, Movie_Index_book, Review_Index_book

  getInit() #init all the books
  
  #Load the dictionary
  Review_dict = loadPockle("./constants/Review_dict")
  print "Size of Review_dict:\t%s" % len(Review_dict.keys())
  
  #Collect Movie_Index_book
  Movie_Index_book = ParseGetMovie_Index(Review_dict)
  print "Size of all Movies in Movie_Index_book:\t%s" % countAllKeysFromBook(Movie_Index_book)

  #Collect Review_Index_book
  Review_Index_book = ParseGetReview_Index(Review_dict)
  print "Size of all Critics in Review_Index_book:\t%s" % countAllKeysFromBook(Review_Index_book)  
  
  print "Dumping Movie_Index_book ..."
  dumpPickle(Movie_Index_book, "./constants/", "Movie_Index")
  print "Dumping Review_Index_book ..."
  dumpPickle(Review_Index_book, "./constants/", "Review_Index")
  print "ReviewIndexing Done ..."

def SearchEngineIndexing():
  global Movie_dict
  getInit() #init all the books

  #Load the dictionary
  Movie_dict = loadPockle("../constants/Movie_dict")
  print "Size of Movie_dict:\t%s" % len(Movie_dict.keys())

  for eachMovie in Movie_dict.keys():
    # print "Title:\t%s\tSynopsis:\t%s" % (Movie_dict[eachMovie]['title'], Movie_dict[eachMovie]['synopsis'])
    print Movie_dict[eachMovie]['synopsis']
    # for eachkey in Movie_dict[eachMovie].keys():
    #   print "Key:\t%s\tValue:%s" % (eachkey, Movie_dict[eachMovie][eachkey])
    # for eachKey in Movie_dict[eachMovie].keys():
    #   print eachKey
    #   print Movie_dict[Movie_dict.keys()[0]][eachKey]
    print "======================================="


if __name__ == "__main__":
  # ReviewIndexing()
  SearchEngineIndexing()




