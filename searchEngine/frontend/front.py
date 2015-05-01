import tornado.httpserver
import tornado.ioloop
import tornado.web
import hashlib
import socket
import getpass

import json

from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.options import define, options

from src import color
bcolors = color.bcolors()

# ## collecting four available ports
ports=[]
ports_index = []
ports_Doc = []

# print "front end: http://linserv2.cims.nyu.edu:" + str(ports[0])

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
        
        K=10
        myquery = self.request.uri        
        print "\n" + bcolors.HEADER + '====== OPERATION RECORD ======'+ bcolors.ENDC    
        print bcolors.LIGHTBLUE + "Searching query: " + myquery + bcolors.ENDC
        # fetching index server
        doc_list=[]
        for i in range(len(ports_index)):            
            toFetch=str(ports_index[i]) + str(myquery.replace('/search?', '/index?'))
            # toFetch="http://linserv2.cims.nyu.edu:" + str(ports_index[i]) + str(myquery.replace('search', 'index'))
            print bcolors.LIGHTBLUE + "Fetching index server " + toFetch + bcolors.ENDC
            http_client = AsyncHTTPClient()                                
            tmp_response = yield http_client.fetch(toFetch)            
            n=json.loads(tmp_response.body)                        
            doc_list.extend(n[n.keys()[0]])            

        
        doc_list.sort(key=lambda x: x[1], reverse=True)
        print bcolors.LIGHTBLUE + "Top" + str(K) + " doc_list after sorting: " + str(doc_list[0:10]) + bcolors.ENDC

        # find the min number
        minN= min(K,len(doc_list))

        # fetching document server
        report=[]
        # body = 'Number of results: %s <br>\n<ol>' % minN
        body = '<font size="5" color="blue">Top %s Number of results:</font><br>\n<ol>' % minN
        for i in range(min(K,len(doc_list))):                                                            
            # print "doc_list[i][0]: " + str(doc_list[i][0])
            toFetch=str(ports_Doc[int(doc_list[i][0])%3]) + "/doc?id=" + str(doc_list[i][0]) + "&" + str(myquery.replace('/search?', ''))
            # toFetch="http://linserv2.cims.nyu.edu:" + str(ports_Doc[doc_list[i][0] %3]) + "/doc?id=" + str(doc_list[i][0]) + "&" + str(myquery.replace('/search?', ''))
            print bcolors.LIGHTBLUE + "Fetching document server " + toFetch + bcolors.ENDC
            http_client = AsyncHTTPClient()                                
            tmp_response = yield http_client.fetch(toFetch)
            n=json.loads(tmp_response.body)
            print "keys: " + str(n.keys())
            # print n
            # print result
            body += '<li><a href=%s>%s</a><br>DocId: %s<br>%s</li>' % (n['url'], n['title'], n['docID'], n['snippet'])            

        body += '</ol>'
        self.write('<html><head><title>SEA search engine</title></head><body>%s</body></html>' % (body))
        


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
        global ports_index, ports_Doc
        ports_index = Idxservers
        ports_Doc = Docservers
        self.app = tornado.httpserver.HTTPServer(Application() )        



# def main():
# 	global ports
# 	tornado.options.parse_command_line()
# 	http_server = tornado.httpserver.HTTPServer(Application() )
# 	http_server.listen(ports[0])
# 	tornado.ioloop.IOLoop.instance().start()

# if __name__ == "__main__":        
# 	main()




