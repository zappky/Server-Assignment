import webapp2
import json #for json format
import re #regrex
import cgi
import urllib
from google.appengine.ext import ndb

from LevelInfo import * # import my levelinfo class
from Player import * # import my player class

#key delieverable
#authentication
#datastore for all data
#all api are working
#correct corresponding response and request

#good to do
#correct response code

class GetPlayerHighestLevel(webapp2.RequestHandler): # get a list of level and number of player with corresponding highest level reach, response in json ,no request
    def get(self):
        pass
    
class GetAverageHighestScore(webapp2.RequestHandler): # get a list of level and average highest score, response in json ,no request
    def get(self):
        pass
    
class GetLevelAttempts(webapp2.RequestHandler): # get a list of level and total attempt, response in json ,no request
    def get(self):
        pass

class GetTotalPlayersNumber(webapp2.RequestHandler): # get number of player, response in json ,no request
    def get(self):
        pass

class GetUserUnlockedLevels(webapp2.RequestHandler): # get a list of unlocked level with high score of a user, response in json ,no request
    def get(self,user_id):
        pass

class GetUserProgress(webapp2.RequestHandler): # get a user,level,high score,pig killed, response in json ,no request
    def get(self,user_id,level):
        pass

class UpdateUserProgress(webapp2.RequestHandler): # update a user ,level,score,pig killed, no response ,request body in json
    def post(self,user_id):
        pass
    
class CreateUser(webapp2.RequestHandler): # create a user, response in json,no request body
    def post(self):
        pass

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    webapp2.Route('/user/create', handler = CreateUser,name = 'CreateUser'),
    webapp2.Route('/user/<user_id:[\w]+>/progress', handler = UpdateUserProgress,name = 'UpdateUserProgress'),
    webapp2.Route('/user/<user_id:[\w]+>/progress/<level:[\d]+>', handler = GetUserProgress,name = 'GetUserProgress'),
    webapp2.Route('/user/<user_id:[\w]+>/unlocked>', handler = GetUserUnlockedLevels,name = 'GetUserUnlockedLevels'),
    webapp2.Route('/admin/players>', handler = GetTotalPlayersNumber,name = 'GetTotalPlayersNumber'),
    webapp2.Route('/admin/level/attempts>', handler = GetLevelAttempts,name = 'GetLevelAttempts'),
    webapp2.Route('/admin/level/average_score>', handler = GetAverageHighestScore,name = 'GetAverageHighestScore'),
    webapp2.Route('/admin/level/highest_level>', handler = GetPlayerHighestLevel,name = 'GetPlayerHighestLevel'),
], debug=True)
#webapp2.Route('/mplayer/<playerid:[a-z]+>', handler = mplayerHandler,name = 'mplayerHandler'),
