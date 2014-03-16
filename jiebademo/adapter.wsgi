# -*- coding: cp936 -*-
import sys, os, bottle
path = '/Users/mac/NLTK/jiebademo/jiebademo'
if path not in sys.path:
    sys.path.append(path)
#sys.path = ['/Users/mac/NLTK/jiebademo/jiebademo'] + sys.path
os.chdir(os.path.dirname(__file__))
import wsgi # This loads your application
#application = bottle.default_app()

from wsgiref.simple_server import make_server
httpd = make_server('localhost', 8104, bottle.default_app())
# Wait for a single request, serve it and quit.
httpd.serve_forever()

