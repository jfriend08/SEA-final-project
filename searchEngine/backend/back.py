import tornado.httpserver
import tornado.ioloop
import tornado.web
import hashlib
import socket
import getpass
import os, re, math
import json
import pickle
import urllib
from nltk.tokenize import RegexpTokenizer

from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.options import define, options

from operator import mul

invertedIndex = None
tokenizer = None
IDF_Index = None


from src import color
bcolors = color.bcolors()

def Tosnippet(text, keywords, extend):
    returnText= '...'    
        
    for keyword in keywords:        
        loc= 0
        tmp= 0
        loc = text.lower().find(keyword.lower(), loc)
        toReplace = text[int(loc):int(loc)+int(len(keyword))]
        text= text.replace(toReplace, '<strong>{}</strong>'.format(toReplace)) + "..."
        loc= 0
        tmp= 0
        while (loc<len(text) and loc!=-1):
            tmp = loc        
            loc = text.lower().find(keyword.lower(), loc)            
            if loc==-1 or loc==tmp:
                break            
            if(loc<len(text) or loc-extend>tmp):
                returnText = returnText + text[loc-extend:loc+extend] + "..."
            elif loc==-1 or loc==tmp:
                break    

    return returnText

def Tosnippet2(text, keywords, extend):
    returnText= '...'    
    locations = {}
    output = ''
    for word in keywords:        
        for m in re.finditer(word.lower(), text.lower()):            
            try:
                locations[word].append((m.start(), m.end()))
            except:
                locations[word] = [(m.start(), m.end())]                     

    for key in locations.keys():
        (start, end)= locations[key][0]
        toReplace = text[start:end]     
        str_start = 0 if (start-extend<0) else start-extend        
        str_end = len(text) if (end+extend>len(text)) else end+extend
        
        tmptext = text[str_start:str_end]                
        output += tmptext.replace(toReplace, '<strong>{}</strong>'.format(toReplace)) + "...<br>"            
    return output


def vectorSpaceCalculation(vectorSpace):
    # vectorSpace stored each token as the key, and its corresponding (docID, TF, idf)s
    
    # multiply all TFidfs if they all have the same docid, and then saved in TFidf_dic
    # so each TFidf_dic[docID] is one 
    TFidf_dic = {}
    TFidf_dic_vectorSpace = {}
    q_space = {}
    for token in vectorSpace.keys():
        for (docid, TF, idf) in vectorSpace[token]:
            value = float(TF)*float(idf)
            try:
                if (value==0):
                    TFidf_dic[docid] = TFidf_dic[docid]
                else:
                    TFidf_dic[docid] = TFidf_dic[docid] * value

                TFidf_dic_vectorSpace[docid].append(value)
            except KeyError:
                TFidf_dic[docid] = value                    
                TFidf_dic_vectorSpace[docid] = [value]

            try:
                q_space[token] = idf
            except KeyError:
                q_space[token] = idf

    # Length of q 
    print "TFidf_dic_vectorSpace:\t%s" % TFidf_dic_vectorSpace
    squ_sum=0
    for k in q_space.keys():        
        squ_sum= squ_sum + q_space[k]*q_space[k]
    q_space_length=math.sqrt(squ_sum)

    resultList = []
    for eachDocID in TFidf_dic.keys():        
        
        # Length of current document
        squ_sum=0        
        for value in TFidf_dic_vectorSpace[eachDocID]:
            squ_sum = squ_sum + value * value
        curDoc_length = math.sqrt(squ_sum)

        # similarity values
        cosSim = TFidf_dic[eachDocID]/(q_space_length*curDoc_length)
        resultList.append((eachDocID,cosSim))

    return resultList
    


class Application(tornado.web.Application):
    def __init__(self, server):
        if(server == 'IndexServer'):            
            handlers = [
                (r"/", HomeHandler),            
                (r"/index", idxSearchHandler)
            ]        
        elif (server == 'DocServer'):            
            handlers = [
                (r"/", HomeHandler),            
                (r"/doc", docSearchHandler)
            ]
        else:
            raise NameError('wrong server name')
        
        tornado.web.Application.__init__(self, handlers)

class idxSearchHandler(tornado.web.RequestHandler):
    @gen.coroutine            
    def get(self):
        global invertedIndex, tokenizer, IDF_Index
        myquery = self.request.uri
        myquery = urllib.unquote(myquery.split('?q=')[-1])
        tokens = [t for t in tokenizer.tokenize(myquery)]                
        # tokens = [t.lower() for t in tokenizer.tokenize(myquery)]                
        print "tokens in idxSearchHandler:\t%s"%tokens        
        vectorSpace = {}
        alllistfromToken = []
        for token in tokens:            
            try:                        
                myidf = IDF_Index[token]                
                myreturns = invertedIndex[token]
                new = []                
                for myid in myreturns.keys():
                    new.append((myid, myreturns[myid], myidf))
                    
                # for i in range(len(myreturns)):                    
                #     (myid, TF) = myreturns[i]
                #     new.append((myid, TF, myidf))
                vectorSpace[token] = new
            except KeyError:
                continue


        # calculate the cosSim for each of vector space and return (docID, TFidf) list        
        alllistfromToken = vectorSpaceCalculation(vectorSpace)

        self.write(json.dumps({'postings': alllistfromToken}))

class docSearchHandler(tornado.web.RequestHandler):
    @gen.coroutine            
    def get(self):
        global invertedIndex, tokenizer, IDF_Index
        myquery = urllib.unquote(self.request.uri)
        docid = self.get_argument('id', None)
        query = self.get_argument('q', None)
        # (docid, query) = myquery.replace('/doc?id=','\t').split("&q=")        
        query=query.split()
        print "docid in Doc Server:\t%s"%docid
        print "query in Doc Server:\t%s"%query        
        # print invertedIndex[docid]['synopsis']

        self.write(json.dumps({ 'url':"http://www.rottentomatoes.com/m/"+invertedIndex[docid]['title'].replace(",", "").replace(".", "").replace(":", "").replace(" - ", "_").replace(" ", "_"),
            'posterurl':invertedIndex[docid]['posters']['profile'],
            'snippet':Tosnippet2(invertedIndex[docid]['synopsis'], query, 50),
            'docID':docid,
            'title':invertedIndex[docid]['title']

            }))
        
        
    
        


        


count=0
class HomeHandler(tornado.web.RequestHandler):
    @gen.coroutine     
    def get(self):      
        global count
        self.write("Reflesh Count:" + str(count))
        count=count+1


class BackEndApp(object):
    def __init__(self, serverType, serverNum, port):
        global invertedIndex, tokenizer, IDF_Index
            
        path2IDF =  './constants/idf/0.out'
        if (serverType=='IndexServer'):
            path = './constants/invertedIndex/' + str(serverNum) + '.out'        
            # path = os.path.dirname(__file__) + '/../../assignment5/constants/Index/' + str(serverNum) + '.out'
        elif (serverType=='DocServer'):
            path = './constants/documentStore/' + str(serverNum) + '.out'            
            # path = os.path.dirname(__file__) + '/../../assignment5/constants/Doc/' + str(serverNum) + '.out'
        else:
            raise NameError('path error')
        
        # load pickle the proper pickle file
        print bcolors.OKGREEN + str(serverType) + ":" + str(port) + " loading: " + str(path) + bcolors.ENDC
        invertedIndex = pickle.load(open(path, 'r'))
        IDF_Index = pickle.load(open(path2IDF, 'r'))
        tokenizer = RegexpTokenizer(r'\w+')
        
        self.app = tornado.httpserver.HTTPServer(Application(serverType) )        

        # http_server = tornado.httpserver.HTTPServer(Application(serverType) )
        # print "listen to:" + str(port)                
        # http_server.listen(port)
        # tornado.ioloop.IOLoop.instance().start()




        