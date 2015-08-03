import webapp2
import json #for json format
import re #regrex
import cgi
import urllib
from google.appengine.ext import ndb

from LevelInfo import * # import my levelinfo class
from Player import * # import my player class

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
