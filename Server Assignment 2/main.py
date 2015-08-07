import webapp2
import json #for json format
import re #regrex
import cgi
import urllib
from google.appengine.ext import ndb

import base64
import hashlib
import uuid

from Admins import * # import my Admin class
from Player import * # import my player class

#key delieverable
#authentication
#datastore for all data
#all api are working
#correct corresponding response and request

#good to do
#correct response code

me = MasterAdmin()

testplayer = Player()
testplayer.SetUserId("playerid")
testplayer.SetSecretKey("password")

testaccountadmin = AccountAdmin()
testaccountadmin.SetUserId("accountadminid")
testaccountadmin.SetSecretKey("password")

testgameadmin = GameAdmin()
testgameadmin.SetUserId("gameadminid")
testgameadmin.SetSecretKey("password")

#currentuser = me
#currentuser.secret_key = hashlib.sha1(str(currentuser.secret_key))
currentuser = None
user_list = [me,testplayer,testaccountadmin,testgameadmin]# for testing only,will need to change to use datastore later

def CreatePlayerAuto():# auto gen a player
    user = Player()
    user_id = uuid.uuid4()
    secret_key = uuid.uuid4()
    hash_secret_key = hashlib.sha1(str(secret_key))
    user.Populate(user_id,hash_secret_key,[])
    return user,secret_key

def AddUser(the_user):# will change to using datastore instead
    user_list.append(the_user)
    
def FindUser(userid):# will change to using datastore instead
    for index in range(len(user_list)):
        if str(user_list[index].GetUserId()) == userid:
            return user_list[index]
    
def DecodeBasicAuth(self):
    authorization = str(self.request.headers.get('Authorization', None))
    
    errormsgflag = False
    
    errormsg = "Bad Authorization"
    
    if authorization == None or authorization == []:
         self.abort(400,errormsg)

    try:
        trash,encoded = authorization.split(' ')
        decoded = base64.b64decode(encoded)
        userid, password = decoded.split(':')
    except:
        self.abort(400,errormsg + " internal error")
        
    
    if userid == '' or  userid == None:
        errormsg += ": userid is empty \n"
        errormsgflag = True
        
    if password == '' or password == None:
        errormsg += " , password is empty \n"
        errormsgflag = True
            
    if errormsgflag:
        self.abort(400,errormsg)
    
        
    return [userid,password]

def BasicAuthCheck(self,the_user = currentuser):
    
    userid , password = DecodeBasicAuth(self)
    
    the_user = FindUser(userid)#just find again regardlessly,this is if, the user suddenly change the crediental on postman
    global currentuser
    currentuser = the_user
    if the_user == None: # if still cannot find user
        self.abort(404,"User cannot be found")
           
    #if the_user == None:
        #the_user = FindUser(userid)
        #global currentuser
        #currentuser = the_user
        #if the_user == None: # if still cannot find user
           #self.abort(404,"User cannot be found")
  
    if the_user.StringUserId() == userid:
        
        user_key = the_user.GetSecretKey()

        if isinstance(user_key,basestring):
            if user_key == password:
                #self.response.write("User Password is correct: " + "this is base STRING validation \n ")
                return True
            else:
                self.abort(400,"User Password is wrong: " + "this is base STRING validation")
                
        testhashsample = hashlib.sha1(str(password))
        digestedsample = testhashsample.hexdigest()
        
        if the_user.StringSecretKey() == digestedsample:
            #self.response.write("User Password is correct: " + "this is HASH validation \n ")
            return True
        else:
            self.abort(400,"User Password is wrong: " + "this is HASH validation")
    else:
        self.abort(400,"User ID is wrong")
        
    return False

def StringMultiClassName(inputlist):
    outputstring = ""
    for index in range(len(inputlist)):
        outputstring += " " + str(inputlist[index].__name__) + ", "
    return outputstring

def MultiUserTypeCheck(allowedtypelist , the_user ):
    for index in range(len(allowedtypelist)):
        if isinstance(the_user,allowedtypelist[index]) == True:
            return True
        
    return False
        
def UserTypeCheck(validtype,theuser):
    return isinstance(theuser,validtype)

def StringUserType(the_user = currentuser):
    return str(the_user.__class__.__name__)

class GetPlayerHighestLevel(webapp2.RequestHandler): # get a list of level and number of player with corresponding highest level reach, response in json ,no request
    def get(self):
        BasicAuthCheck(self,currentuser)

        #if not UserTypeCheck(GameAdmin,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        AllowedUserTypeList = [GameAdmin]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))
             
        self.response.set_status(200)
    
class GetAverageHighestScore(webapp2.RequestHandler): # get a list of level and average highest score, response in json ,no request
    def get(self):
        BasicAuthCheck(self,currentuser)

        #if not UserTypeCheck(GameAdmin,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        AllowedUserTypeList = [GameAdmin]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))
            
        self.response.set_status(200)
    
class GetLevelAttempts(webapp2.RequestHandler): # get a list of level and total attempt, response in json ,no request
    def get(self):
        BasicAuthCheck(self,currentuser)

        #if not UserTypeCheck(GameAdmin,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        AllowedUserTypeList = [GameAdmin]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))
             
        self.response.set_status(200)

class GetTotalPlayersNumber(webapp2.RequestHandler): # get number of player, response in json ,no request
    def get(self):
        BasicAuthCheck(self,currentuser)

        #if not UserTypeCheck(GameAdmin,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        AllowedUserTypeList = [GameAdmin]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))
               
        self.response.set_status(200)

class GetUserUnlockedLevels(webapp2.RequestHandler): # get a list of unlocked level with high score of a user, response in json ,no request
    def get(self,user_id):
        BasicAuthCheck(self,currentuser)

        #if not UserTypeCheck(Player,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        AllowedUserTypeList = [Player]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))
               
        self.response.set_status(200)

class GetUserProgress(webapp2.RequestHandler): # get a user,level,high score,pig killed, response in json ,no request
    def get(self,user_id,level):
        BasicAuthCheck(self,currentuser)

        #if not UserTypeCheck(Player,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        AllowedUserTypeList = [Player]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))
              
        self.response.set_status(200)

class UpdateUserProgress(webapp2.RequestHandler): # update a user ,level,score,pig killed, no response ,request body in json
    def post(self,user_id):
        BasicAuthCheck(self,currentuser)

        #if not UserTypeCheck(Player,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        
        AllowedUserTypeList = [Player]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))
            
        self.response.set_status(200)
        
class CreateUser(webapp2.RequestHandler): # create a user, response in json,no request body
    def post(self):
        BasicAuthCheck(self,currentuser)

        #if not UserTypeCheck(AccountAdmin,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
            #self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) + "Account Admin and Master Admin allowed")
        AllowedUserTypeList = [AccountAdmin,MasterAdmin]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))
        
        self.response.headers['Content-Type'] = 'application/json'
        newuser,originalkey = CreatePlayerAuto()
        AddUser(newuser)
        
        jsonobj = {
            'user_id': str(newuser.GetUserId()), 
            'secret_key': str(originalkey),
        } 
        self.response.out.write(json.dumps(jsonobj, sort_keys = True, indent = 4 , separators = (',', ': ')) )
        self.response.set_status(201)
        
class DebugUserHandler(webapp2.RequestHandler):# print out the users
    def get(self):
        if currentuser != None:
            self.response.write("Current User: " + currentuser.StringSelf()+ "<br> Type: " + StringUserType(currentuser) + "<br>")
        
        responsestring = ""
        for index in range(len(user_list)):
            responsestring += "<br>" + " index:" + "<"+ str(index) +">"+ "<br> Type: " + StringUserType(user_list[index])+ user_list[index].StringSelf() +"<br>"
            
        self.response.write(responsestring)
        
class DebugHandler(webapp2.RequestHandler):# set debug parameters
    def get(self):
        self.response.write('Hello Debug!')
        usertype = self.request.get("usertype")
        global currentuser
        if usertype == "masteradmin":
            currentuser = me
        elif usertype == "gameadmin":
            currentuser = testgameadmin
        elif usertype == "accountadmin":
            currentuser = testaccountadmin
        elif usertype == "player":
            currentuser = testplayer
        else:
            currentuser = None
            
        self.response.write('<br> currentuser type is: ' + currentuser.__class__.__name__)
        
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    webapp2.Route('/debug', handler = DebugHandler,name = 'DebugHandler'),
    webapp2.Route('/debug/currentuser', handler = DebugUserHandler,name = 'DebugUserHandler'),
    webapp2.Route('/user/create', handler = CreateUser,name = 'CreateUser'),
    webapp2.Route('/user/create/', handler = CreateUser,name = 'CreateUser'),
    webapp2.Route('/user/<user_id:[\w]+>/progress', handler = UpdateUserProgress,name = 'UpdateUserProgress'),
    webapp2.Route('/user/<user_id:[\w]+>/progress/', handler = UpdateUserProgress,name = 'UpdateUserProgress'),
    webapp2.Route('/user/<user_id:[\w]+>/progress/<level:[\d]+>', handler = GetUserProgress,name = 'GetUserProgress'),
    webapp2.Route('/user/<user_id:[\w]+>/progress/<level:[\d]+>/', handler = GetUserProgress,name = 'GetUserProgress'),
    webapp2.Route('/user/<user_id:[\w]+>/unlocked>', handler = GetUserUnlockedLevels,name = 'GetUserUnlockedLevels'),
    webapp2.Route('/user/<user_id:[\w]+>/unlocked>/', handler = GetUserUnlockedLevels,name = 'GetUserUnlockedLevels'),
    webapp2.Route('/admin/players', handler = GetTotalPlayersNumber,name = 'GetTotalPlayersNumber'),
    webapp2.Route('/admin/players/', handler = GetTotalPlayersNumber,name = 'GetTotalPlayersNumber'),
    webapp2.Route('/admin/level/attempts', handler = GetLevelAttempts,name = 'GetLevelAttempts'),
    webapp2.Route('/admin/level/attempts/', handler = GetLevelAttempts,name = 'GetLevelAttempts'),
    webapp2.Route('/admin/level/average_score', handler = GetAverageHighestScore,name = 'GetAverageHighestScore'),
    webapp2.Route('/admin/level/average_score/', handler = GetAverageHighestScore,name = 'GetAverageHighestScore'),
    webapp2.Route('/admin/level/highest_level', handler = GetPlayerHighestLevel,name = 'GetPlayerHighestLevel'),
    webapp2.Route('/admin/level/highest_level/', handler = GetPlayerHighestLevel,name = 'GetPlayerHighestLevel'),
], debug=True)
