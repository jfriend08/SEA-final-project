import tornado.httpserver
import tornado.ioloop
import tornado.web
import hashlib
import socket
import getpass

import json, pickle

from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.options import define, options

from src import color
bcolors = color.bcolors()

# ## collecting four available ports
ports=[]
ports_index = []
ports_Doc = []
genere_dict = {}

def remove_duplicates(mylist):
    output = []
    seen = set()
    for (movieID, value) in mylist:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if movieID not in seen:
            output.append((movieID, value))
            seen.add(movieID)
    return output

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),            
            (r"/search", SearchHandler),
            (r'/(\d{4})/(\d{2})/(\d{2})/([a-zA-Z\-0-9\.:,_]+)/?', DetailHandler)            
        ]        
        tornado.web.Application.__init__(self, handlers)

class SearchHandler(tornado.web.RequestHandler):
    @gen.coroutine            
    def get(self):
        global genere_dict        
        NumIndexServer = len(ports_index)
        NumDocServer = len(ports_Doc)
        K=10
        # myquery = self.request.uri                
        myquery = self.get_argument('q', None)    
        genre =  self.get_argument('genre', None)    

        myquery =  self.get_argument('q', None)    
        print "\n" + bcolors.HEADER + '====== OPERATION RECORD ======'+ bcolors.ENDC    
        print bcolors.LIGHTBLUE + "Searching query: " + myquery + bcolors.ENDC
        print "genre!!!!!!!!%s"%genre
        
        # fetching index server
        doc_list=[]
        for i in range(len(ports_index)):            
            toFetch="%s/index?q=%s" %(ports_index[i], myquery.replace(" ", "%20"))            
            print bcolors.LIGHTBLUE + "Fetching index server " + toFetch + bcolors.ENDC
            http_client = AsyncHTTPClient()                                
            tmp_response = yield http_client.fetch(toFetch)            
            n=json.loads(tmp_response.body)                        
            doc_list.extend(n[n.keys()[0]])            

        
        doc_list.sort(key=lambda x: x[1], reverse=True)
        doc_list = remove_duplicates(doc_list[0:K])
        print bcolors.LIGHTBLUE + "Top" + str(K) + " doc_list after sorting: " + str(doc_list[0:K]) + bcolors.ENDC        
        
        # find the min number
        minN= min(K,len(doc_list))

        # fetching document server
        report=[]
        # body = 'Number of results: %s <br>\n<ol>' % minN
        body = '<font size="5" color="blue">Top %s search results:</font><br>\n<ol>' % minN
        
        NormalResult = []
        GenreResult = []

        for i in range(min(K,len(doc_list))):                                                            
            
            Docidx = hash(str(doc_list[i][0]))%NumDocServer
            print "Docidx in front end:%s"%Docidx            
            toFetch="%s/doc?id=%s&q=%s" %(ports_Doc[Docidx], doc_list[i][0],myquery.replace(" ", "%20"))            
            
            print bcolors.LIGHTBLUE + "Fetching document server " + toFetch + bcolors.ENDC
            http_client = AsyncHTTPClient()                                
            tmp_response = yield http_client.fetch(toFetch)
            n=json.loads(tmp_response.body)
            

            Highlight_bit = False
            try:
                for cur_gener in genere_dict[str(n['docID'])]:
                    # print "cur_gener:%s"%cur_gener
                    # print "genre:%s"%genre
                    if cur_gener in genre:
                        Highlight_bit = True
                        break
            except:
                pass

            if Highlight_bit:
                body += '<li><a href=%s><font color="red">%s</font></a><br>DocId: %s<br>%s<br><img src=%s alt="HTML5 Icon" ></li>' % (n['url'], n['title'], n['docID'], n['snippet'], n['posterurl'])
                NormalResult.append([n['url'], n['title'], n['docID'], n['snippet'], n['posterurl']])
                GenreResult.append([n['url'], n['title'], n['docID'], n['snippet'], n['posterurl']])
            else:
                body += '<li><a href=%s>%s</a><br>DocId: %s<br>%s<br><img src=%s alt="HTML5 Icon" ></li>' % (n['url'], n['title'], n['docID'], n['snippet'], n['posterurl'])
                NormalResult.append([n['url'], n['title'], n['docID'], n['snippet'], n['posterurl']])

        body += '</ol>'
        print "NormalResult\n%s" % NormalResult
        print "GenreResult\n%s" % GenreResult
        
        toSuperFront={}
        toSuperFront['NormalResult'] = NormalResult
        toSuperFront['GenreResult'] = GenreResult
        
        self.write(json.dumps(toSuperFront))
        # self.write('<html><head><title>SEA search engine</title></head><body>%s</body></html>' % (body))
        


count=0
class HomeHandler(tornado.web.RequestHandler):
    @gen.coroutine     
    def get(self):      
        global count
        self.write("Reflesh Count:" + str(count))
        count=count+1

class DetailHandler(tornado.web.RequestHandler):
    def get(self, year, month, day, slug):
        self.write("DetailHandler:" + str(slug))

class FrontEndApp(object):
    def __init__(self, Idxservers, Docservers):
        global ports_index, ports_Doc, genere_dict
        ports_index = Idxservers
        ports_Doc = Docservers
        genere_dict = pickle.load(open("./constants/genreIndexer/0.out", 'r'))
        self.app = tornado.httpserver.HTTPServer(Application() )        



# def main():
#   global ports
#   tornado.options.parse_command_line()
#   http_server = tornado.httpserver.HTTPServer(Application() )
#   http_server.listen(ports[0])
#   tornado.ioloop.IOLoop.instance().start()

# if __name__ == "__main__":        
#   main()




