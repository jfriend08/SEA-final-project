import nltk
import math
import re
import pickle
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from xml.etree.ElementTree import iterparse
import urllib
import socket
from sklearn.feature_extraction.text import TfidfTransformer

from constants import color
bcolors = color.bcolors()

class Indexer(object):
  def __init__(self, Idxserver, Docserver):
    self.numIndex = len(Idxserver); #to remember the number of index server
    self.numDoc = len(Docserver); #to remember the number of document server
    self.IdxServerBook = {}; #IdxServerBook[serverAddress][term] -> [(docId, TF) ... (docId, TF)]
    self.DocServerBook = {};
    self.docId = 0; #to store the currnt docId
    self.TermBook = {}; #TermBook[term] -> global total count
    self.numPage = 0; #Number of pages    

    for i in range(self.numIndex):      
      self.IdxServerBook[Idxserver[i] ] = {}
    for i in range(self.numDoc):      
      self.DocServerBook[Docserver[i] ] = {}
  
  def genNum(self):    
    print bcolors.OKGREEN + "Indexer start" + bcolors.ENDC    

  def getXML(self, path, Idxserver, Docserver):
    print bcolors.OKGREEN + "Importing XML" + bcolors.ENDC
    myBase, allInfo = importXML(path)    
    self.numPage = len(allInfo)

    
    for title, token_dic, content in allInfo:
      cur_docId = self.docId
      self.docId += 1
      
      cur_IdxServer = Idxserver[cur_docId % self.numIndex]
      cur_DocServer = Docserver[cur_docId % self.numDoc]

      for term, local_TF_inDoc in token_dic.iteritems():                
        
        #assign initial terms to IdxServerBook with (docId, local_TF) appended
        try:                    
          self.IdxServerBook[cur_IdxServer][term].append((cur_docId, local_TF_inDoc) )           
        except:
          self.IdxServerBook[cur_IdxServer][term] = [(cur_docId, local_TF_inDoc)]          

        # tring to collect the global occurnce of each terms into TermBook
        try:
          self.TermBook[term] += 1
        except:                
          self.TermBook[term] = 1
      
      #assign info to DocServerBook
      self.DocServerBook[cur_DocServer][cur_docId] = {
        'title': title,
        'url': myBase.replace('Main_Page', title),
        'text': content      
      }
    
    #calcuting TF.IDF
    #each of the original TF is globally normalized by log(totalPage/number of occurance)
    for eachServer in Idxserver:            
      for term, allIDpairs in self.IdxServerBook[eachServer].iteritems():        
        newPairs=[]
        for myid, tf in allIDpairs:                  
          idf = math.log( self.numPage/self.TermBook[term] )
          # tf = tf * math.log( self.numPage/self.TermBook[term] )
          # A bonus should be given to terms that appear in the title
          if term in self.DocServerBook[Docserver[myid % self.numDoc]][myid]['title'].split():
            tf = tf * 1.5
          newPairs.append((myid, tf, idf) )        
        self.IdxServerBook[eachServer][term] = newPairs        
      


    # print "local structural count: " + str(self.IdxServerBook[ Idxserver[110%3] ]['structural']) + " global structural count: " + str(self.TermBook['structural'])
    # # print self.IdxServerBook[ Idxserver[215%3] ]['represents']
    # print self.IdxServerBook[ Idxserver[0] ]['personalized']
    # print self.IdxServerBook[ Idxserver[1] ]['personalized']
    # print self.IdxServerBook[ Idxserver[2] ]['personalized']
    # print self.TermBook['personalized']
    # print self.TermBook['the']    
    # print self.DocServerBook[Docserver[186%3]][186]

    
    #Index servers. use pickle to save IdxServerBook
    for i in range(len(self.IdxServerBook)):      
      filename = './pickle/indexServer' + str(i)
      fileObj = open(filename, 'w')
      print bcolors.OKGREEN + "Saving pickle for Index Server: " + Idxserver[i] + bcolors.ENDC
      pickle.dump(self.IdxServerBook[Idxserver[i]], fileObj)
      fileObj.close()    

    #Document servers. use pickle to save DocServerBook
    for i in range(len(self.DocServerBook)):      
      filename = './pickle/docServer' + str(i)
      fileObj = open(filename, 'w')
      print bcolors.OKGREEN + "Saving pickle for Document Server: " + Docserver[i] + bcolors.ENDC
      pickle.dump(self.DocServerBook[Docserver[i]], fileObj)
      fileObj.close()    

    
    


#this will load the file path, parse each page, tokenize the content
#
def importXML(path):    
  header = open(path).readline()
  start = header.find('xmlns=')+7  
  NS = "{%s}" % header[start: header.find('\"', start)]  
  allInfo=[] #to store all the concised info
  myBase='' #to store the base web
  with open(path) as f:
    for event, elem in iterparse(f):      
      # print elem.tag #each elem has its own tag      
      if elem.tag == '{0}base'.format(NS):
        myBase = str(elem.text)

      if elem.tag == '{0}page'.format(NS):        
        
        title = elem.find("{0}title".format(NS))
        contr = elem.find(".//{0}username".format(NS))
        content = elem.find(".//{0}text".format(NS))

        token_dic={} #to parse the content into many tokens and store in the dictionary
        if content is not None:            
            tokenizer = RegexpTokenizer(r'\w+') #so can get rid of punctuation
            # print tokenizer.tokenize(content.text)                                    
            for eachword in tokenizer.tokenize(content.text):                            
              try:
                token_dic[eachword.lower()] += 1
              except:
                token_dic[eachword.lower()] = 1

        allInfo.append((title.text, token_dic, content.text))
        elem.clear()  
  
  return myBase, allInfo


# def main():
#   myindexer=Indexer()
#   myindexer.genNum()
#   myindexer.getXML('./info_ret.xml')

# if __name__ == "__main__":        
#   main()

