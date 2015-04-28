import tornado.httpserver
import tornado.ioloop
import tornado.web
import hashlib
import socket
import getpass
import urllib,re, zlib,time
import pickle
import json, sys
import uuid #to create unique user ID
import random #to choose the movie randomly




'''
Goal: 
As of now we don't have the user log for their preference. 
So the gaol of this is to create fake user logs for testing purpose. 

Output:
Everything will be save to myUserBook:
each key is the userID, and value is a list of tuple of (movieID, score)

e.g.
myUserBook[myUserBook.keys()[0]] --> 
[(u'770876743', 70), (u'770691000', 31), (u'770817136', 99), (u'9818', 63), (u'771362832', 34), (u'771040382', 37), (u'770997081', 96), (u'770677279', 63), (u'771385207', 40), (u'19676', 29), (u'771316594', 8), (u'770809742', 4), (u'593947395', 58), (u'21952', 81), (u'770710586', 47), (u'770942327', 6), (u'770845651', 56), (u'17019', 75), (u'753391596', 50), (u'771009897', 0)]

myUserBook will be pickle dumped to userLog/myUserBook

'''


def loadPockle(path):  
  mydict = pickle.load(open(path, 'r'))  
  return mydict 

def dumpPickle(book, path, prefix):  
  filename = path + prefix
  fileObj = open(filename, 'w')
  pickle.dump(book, fileObj)    
  fileObj.close() 

def main():
  Review_dict = loadPockle("../constants/Review_dict")  
  allMovie = Review_dict.keys()
  myUserBook = {}
  for numUser in range(50):
    thisUserID = str(uuid.uuid4()  )
    myUserBook[thisUserID] = []
    for numReview in range (20):
      rand_chooseMovie = Review_dict.keys()[random.randrange(0, len(allMovie))]
      rand_chooseScore = random.randrange(0, 100)
      myUserBook[thisUserID].append((rand_chooseMovie, rand_chooseScore))

  
  print myUserBook.keys()[0]
  print myUserBook[myUserBook.keys()[0]]
  dumpPickle(myUserBook, "../userLog/", "myUserBook")



if __name__ == "__main__":
  main()

