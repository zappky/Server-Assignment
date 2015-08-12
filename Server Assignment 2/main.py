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
me.SetSecretKey("password")

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

MAX_PIG_COUNT = 5# max pig count per stage

SERVER_MODE = True

def SetServerMode(mode):
    global SERVER_MODE
    if mode != None:  
        try:
            SERVER_MODE = mode#serve as live code mode
        except:
            SERVER_MODE = SERVER_MODE #dont touch
    
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

def BasicAuthWithUrl(self,user_id):#using userid passing using url
    #hmm where do i get password for this?
    userid , password = DecodeBasicAuth(self)
    BasicAuth(self,user_id,password)

def BasicAuthWithRequest(self):# using data from auth from request header
    user_id , password = DecodeBasicAuth(self)
    BasicAuth(self,user_id,password)

def BasicAuth(self,user_id,password):
    the_user = FindUser(user_id)#just find again regardlessly,this is if, the user suddenly change the crediental on postman
    global currentuser
    currentuser = the_user
    if the_user == None: # if still cannot find user
        self.abort(404,"User cannot be found, Hint: Check your username")
  
    if the_user.StringUserId() == user_id:
        
        user_key = the_user.GetSecretKey()

        if SERVER_MODE == True:
            if isinstance(user_key,basestring):
                testhashsample = hashlib.sha1(str(password))
                digestedsample = testhashsample.hexdigest()
                if user_key == digestedsample:
                    return True
                else:
                    self.abort(400,"User Password is wrong: " + "this is base STRING validation of hashed password")

                self.abort(400,"Unhandled abort, User Password cannot be validated" )    
            else:
                self.abort(400,"Unhandled password type, User Password cannot be validated" )    
        else:
            #Old method before migation of data to datastore,only work before migation
            if isinstance(user_key,basestring):
                if user_key == password:
                    #self.response.write("User Password is correct: " + "this is base STRING validation \n ")
                    return True
                else:
                    self.abort(400,"User Password is wrong: " + "this is base STRING validation")
            try:       
                testhashsample = hashlib.sha1(str(password))
                digestedsample = testhashsample.hexdigest()
            except TypeError:
                self.abort(400,"Password type error,cannot be digested")
            except:
                self.abort(400,"Unknown error, password cannot be digested")
                
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

def PadEmptyElementForList(the_list,desire_size,element_to_pad):
        list_size = len(the_list)
        if desire_size <= list_size:#escape if invalid request
            return
        pad_amount = desire_size - list_size
        for i in range(pad_amount):
            the_list.append(element_to_pad)

def CreatePlayerAuto():# auto gen a player
    user = Player()
    user_id = uuid.uuid4()
    secret_key = uuid.uuid4()
    hash_secret_key = hashlib.sha1(str(secret_key))
    if SERVER_MODE:
        user.Populate(str(user_id),hash_secret_key.hexdigest(),None)#dunno how to store as hash and/or uuid data,so store them as string instead =X
    else:
        user.Populate(user_id,hash_secret_key,None)
    return user,secret_key

def AddUserLocal(webapp2_handler,the_user):
    user_list.append(the_user)
def AddUserServer(webapp2_handler,the_user):
    try:
        the_user.put()
    except TypeError:
        abort_flag = True
        webapp2_handler.abort(400,"Bad user type,cannot put to datastore")
    except:
        abort_flag = True
        webapp2_handler.abort(400,"Unknown error ,Bad user data,cannot put to datastore")
def AddUser(webapp2_handler,the_user):
    if SERVER_MODE:
        return AddUserServer(webapp2_handler,the_user)
    return AddUserLocal(webapp2_handler,the_user)
    
    
def FindUserlocal(userid):
    for index in range(len(user_list)):
        if str(user_list[index].GetUserId()) == userid:
            return user_list[index]
    return None
def FindUserServer(userid):
    accountadminquery = AccountAdmin.query(AccountAdmin.user_id == userid).fetch(1)
    gameadminquery = GameAdmin.query(GameAdmin.user_id == userid).fetch(1)
    playerquery = Player.query(Player.user_id == userid).fetch(1)
    masteradminquery = MasterAdmin.query(MasterAdmin.user_id == userid).fetch(1)

    resultquery = masteradminquery + accountadminquery + gameadminquery + playerquery
    if len(resultquery) > 0:#if got result
        return resultquery[0]#return its entity
    return None
def FindUser(userid):
    if SERVER_MODE:
        return FindUserServer(userid)
    return FindUserlocal(userid)
    
def GetAllUserLocal():
    return user_list
def GetAllUserServer():#get all user,include admins
    accountadminquery = AccountAdmin.query().fetch()
    gameadminquery = GameAdmin.query().fetch()
    playerquery = Player.query().fetch()
    masteradminquery = MasterAdmin.query().fetch()

    resultquery = masteradminquery + accountadminquery + gameadminquery + playerquery
    
    if len(resultquery) > 0:#if got result
        return resultquery#return its entity
    return None
def GetAllUser():
    if SERVER_MODE:
        return GetAllUserServer()
    return GetAllUserLocal()

def GetAllPlayerLocal():
    resultlist = []
    for element in user_list:
        if isinstance(element,Player):
            resultlist.append(element)
    return resultlist
def GetAllPlayerServer():#get all user,include admins
    resultquery = Player.query().fetch()
    if len(resultquery) > 0:#if got result
        return resultquery#return its entity
    return None
def GetAllPlayer():
    if SERVER_MODE:
        return GetAllPlayerServer()
    return GetAllPlayerLocal()

def GetAllAdminLocal():
    resultlist = []
    for element in user_list:
        if isinstance(element,Admin):
            resultlist.append(element)
    return resultlist
def GetAllAdminServer():#get all user,include admins
    accountadminquery = AccountAdmin.query().fetch()
    gameadminquery = GameAdmin.query().fetch()
    masteradminquery = MasterAdmin.query().fetch()

    resultquery = masteradminquery + accountadminquery + gameadminquery
    
    if len(resultquery) > 0:#if got result
        return resultquery#return its entity
    return None
def GetAllAdmin():
    if SERVER_MODE:
        return GetAllAdminServer()
    return GetAllAdminLocal()
    
def CountAllUserLocal():
    return len(user_list)
def CountAllPlayerServer():
    userlist = GetAllPlayerServer()
    try:
        return len(userlist)
    except:
        return 0
def CountAllUserServer():
    userlist = GetAllUserServer()
    try:
        return len(userlist)
    except:
        return 0
def CountAllUser():
    if SERVER_MODE:
        return CountAllUserServer(the_user)
    return CountAllUserLocal(the_user)
    
class GameLogicController():
    
    def UpdatePlayerProgress(self,webapp2_handler,the_user,level_number,score,pigs_killed):# for api 2
        
        errorflag = False
        errormsg = "ERROR: "
        
        #None value check
        if pigs_killed == None:
            errorflag = True
            errormsg += "None valued pig killed count is not allowed "
        if score == None:
            errorflag = True
            errormsg += "None valued score is not allowed "
        if level_number == None:
            errorflag = True
            errormsg += "None valued level_number is not allowed "

        if errorflag:
            webapp2_handler.abort(400,errormsg)

        
        #check for number and non-empty string # negative number is accepted here,because i want to error log it better below
        validReg = re.match('[-0-9]+', pigs_killed)
        if not validReg:
            errorflag = True
            errormsg += " Either non-number is input or nothing is input for pig killed count"
        validReg = re.match('[-0-9]+', score)
        if not validReg:
            errorflag = True
            errormsg += " Either non-number is input or nothing is input for score"
        validReg = re.match('[-0-9]+', level_number)
        if not validReg:
            errorflag = True
            errormsg += " Either non-number is input or nothing is input for level"
            
        if errorflag:
            webapp2_handler.abort(400,errormsg)
            
        #type casting from string to int,it would be string because we supposely get them from the request handler    
        pigs_killed = int(pigs_killed)
        score = int(score)
        level_number = int(level_number)
        
        # negative value checks
        if pigs_killed < 0:
            webapp2_handler.abort(400,"Negative valued pig killed count is not allowed : Your Value is " + str(pigs_killed))
        if score < 0:
            webapp2_handler.abort(400,"Negative valued score is not allowed : Your Value is " + str(score))
        if level_number <= 0:
            webapp2_handler.abort(400,"Only non-zero postive valued level_number is allowed : Your Value is " + str(level_number))

        #check if valid level
        if level_number > the_user.GetLevelUnlockedCount():
            webapp2_handler.abort(400,"Player Unlocked Level Count: "+ str(the_user.GetLevelUnlockedCount())+" level number is more than player unlocked level count : Your Value is " + str(level_number))

        #change it into index
        level_index = level_number-1
        #webapp2_handler.response.write("Level index deduced: " + str(level_index))

        #check more bad value
        if pigs_killed > MAX_PIG_COUNT:
            webapp2_handler.abort(400,"More pig killed than a stage have is not allowed : Your Value is " + str(pigs_killed))
        
        the_user.IncrementLevelTotalAttempts(level_index,1)#increment the level total attempt by 1,regardlessly whether the player killed all 5 pig or whether he achieve high score

        #update pig_killed count,but since the game design only allow update player progress when levle is cleared,which is 5 pig only, realistically the only value allowed to update is 5
        if pigs_killed < MAX_PIG_COUNT:
            webapp2_handler.abort(400,"Not all pig have been killed,so cannot update player progress : Your Value is " + str(pigs_killed))
        else:
            the_user.SetLevelPigsKilled(level_index,pigs_killed)# should be 5 anyway
            
        the_user.PadEmptyLevelInfo(level_number+1)#unlock next level by creating empty level info data#whether the player achieve high score, just unlocked next level since pigs_killed count has been validated
        
        #update high score
        if score >= the_user.GetLevelHighestScore(level_index):
            the_user.SetLevelHighestScore(level_index,score)
        else:
            webapp2_handler.abort(400,"Player High Score: "+ str(the_user.GetLevelHighestScore(level_index))+" Only higher score can be record : Your Value is " + str(score))


GLC = GameLogicController()

#game admin account api starts
class GetPlayerHighestLevel(webapp2.RequestHandler): # get a list of level and number of player with corresponding highest level reach, response in json ,no request
    def get(self):
        BasicAuthWithRequest(self)
        #if not UserTypeCheck(GameAdmin,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        AllowedUserTypeList = [GameAdmin]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))
             
        self.response.headers['Content-Type'] = 'application/json'

        jsonobjlist = []
        user_list = []
        
        if SERVER_MODE:
            user_list = GetAllPlayerServer()
        else:
            user_list = GetAllUserLocal()
                
        totathighestlevelreached_list = [0]# index 0 represent level 1's total player highest level reached and so on
        
        for x in range(len(user_list)): #look into each player
            the_player = user_list[x]
            the_player_levellist = the_player.GetLevelInfoList()
            PadEmptyElementForList(totathighestlevelreached_list,len(the_player_levellist),0)
            totathighestlevelreached_list[the_player.GetLevelUnlockedCount()-1] += 1
        
        for i in range(len(totathighestlevelreached_list)):
            jsonobjlist.append( {'level':str(i+1) , 'players':str(totathighestlevelreached_list[i])} )   
       
        self.response.out.write(json.dumps(jsonobjlist, sort_keys = False, indent = 4 , separators = (',', ': ')) )
        
        self.response.set_status(200)
    
class GetAverageHighestScore(webapp2.RequestHandler): # get a list of level and average highest score, response in json ,no request
    def get(self):
        BasicAuthWithRequest(self)

        #if not UserTypeCheck(GameAdmin,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        AllowedUserTypeList = [GameAdmin]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))
            
        self.response.headers['Content-Type'] = 'application/json'

        jsonobjlist = []

        if SERVER_MODE:
            user_list = GetAllPlayerServer()
        else:
            user_list = GetAllUserLocal()
                
        totathighscore_list = [0]# index 0 represent level 1's high score and so on
        totaluserperlevel_list = [0]# parallel list with totathighscore_list# use to indicate amount of user per level
        
        for x in range(len(user_list)): #look into each player
            the_player = user_list[x]
            the_player_levellist = the_player.GetLevelInfoList()
            PadEmptyElementForList(totathighscore_list,len(the_player_levellist),0)
            PadEmptyElementForList(totaluserperlevel_list,len(totathighscore_list),0)
            for y in range(len(the_player_levellist)):
                totathighscore_list[y] += the_player_levellist[y].GetHighestScore()
                totaluserperlevel_list[y] += 1#mark one player
        
        for i in range(len(totathighscore_list)):
            totathighscore_list[i] = totathighscore_list[i]/totaluserperlevel_list[i]
            jsonobjlist.append( {'level':str(i+1) , 'average_score':str(totathighscore_list[i])} )   
       
        self.response.out.write(json.dumps(jsonobjlist, sort_keys = False, indent = 4 , separators = (',', ': ')) )
        
        self.response.set_status(200)
    
class GetLevelAttempts(webapp2.RequestHandler): # get a list of level and total attempt, response in json ,no request
    def get(self):
        BasicAuthWithRequest(self)

        #if not UserTypeCheck(GameAdmin,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        AllowedUserTypeList = [GameAdmin]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))

        self.response.headers['Content-Type'] = 'application/json'

        jsonobjlist = []

        user_list = []
        
        if SERVER_MODE:
            user_list = GetAllPlayerServer()
        else:
            user_list = GetAllUserLocal()
                
        totatattempt_list = [0]# index 0 represent level 1's total attemp and so on
        
        for x in range(len(user_list)): #look into each player
            the_player = user_list[x]
            the_player_levellist = the_player.GetLevelInfoList()
            PadEmptyElementForList(totatattempt_list,len(the_player_levellist),0)
            for y in range(len(the_player_levellist)):
                totatattempt_list[y] += the_player_levellist[y].GetTotalAttempts()
        
        for i in range(len(totatattempt_list)):
            jsonobjlist.append( {'level':str(i+1) , 'total_attempts':str(totatattempt_list[i])} )   
       
        self.response.out.write(json.dumps(jsonobjlist, sort_keys = False, indent = 4 , separators = (',', ': ')) )
        
        self.response.set_status(200)

class GetTotalPlayersNumber(webapp2.RequestHandler): # get number of player, response in json ,no request
    def get(self):
        BasicAuthWithRequest(self)

        #if not UserTypeCheck(GameAdmin,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        AllowedUserTypeList = [GameAdmin]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))

        self.response.headers['Content-Type'] = 'application/json'
        
        totalplayercount = 0
        
        if SERVER_MODE:
            totalplayercount = CountAllPlayerServer()
        else:
            totalplayercount = CountAllPlayerLocal()
        
        jsonobj = {
            'total_players': str(totalplayercount)
        } 
        self.response.out.write(json.dumps(jsonobj, sort_keys = False, indent = 4 , separators = (',', ': ')) )
  
        self.response.set_status(200)
#game admin account api ends
        
#player account api starts   
class GetUserUnlockedLevels(webapp2.RequestHandler): # get a list of unlocked level with high score of a user, response in json ,no request
    def get(self,user_id):
        #BasicAuthCheck(self,currentuser)
        BasicAuthWithUrl(self,user_id)
        #if not UserTypeCheck(Player,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        AllowedUserTypeList = [Player]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))

        self.response.headers['Content-Type'] = 'application/json'

        jsonobjlist = []
        playerlevellist = currentuser.GetLevelInfoList()

        for i in range(len(playerlevellist)):
            jsonobjlist.append( {'level':str(i+1) , 'highest_score':str(playerlevellist[i].GetHighestScore())} )

        self.response.out.write(json.dumps(jsonobjlist, sort_keys = False, indent = 4 , separators = (',', ': ')) )  
        self.response.set_status(200)

class GetUserProgress(webapp2.RequestHandler): # get a user,level,high score,pig killed, response in json ,no request
    def get(self,user_id,level):
        #BasicAuthCheck(self,currentuser)
        BasicAuthWithUrl(self,user_id)
        #if not UserTypeCheck(Player,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        AllowedUserTypeList = [Player]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))

        #none value check , alphabet check are all skipped due to routing limiting to \d which only allow number to pass through
        #type casting from string to int,it would be string because we supposely get them from the url
        level = int(level)

        # negative value checks
        if level <= 0:
            self.abort(400,"Only non-zero postive valued level is allowed : Your Value is " + str(level))

        #check if valid level
        if level > currentuser.GetLevelUnlockedCount():
            self.abort(400,"Player Unlocked Level Count: "+ str(currentuser.GetLevelUnlockedCount())+" level number is more than player unlocked level count : Your Value is " + str(level))

        #change it into index
        level_index = level-1
        
        self.response.headers['Content-Type'] = 'application/json'
        
        jsonobj = {
            'level': str(level), 
            'highest_score': str(currentuser.GetLevelHighestScore(level_index)),
            'pigs_killed': str(currentuser.GetLevelPigsKilled(level_index)),
        } 
        self.response.out.write(json.dumps(jsonobj, sort_keys = False, indent = 4 , separators = (',', ': ')) )
        self.response.set_status(200)

class UpdateUserProgress(webapp2.RequestHandler): # update a user ,level,score,pig killed, no response ,request body in json
    def post(self,user_id):
        #BasicAuthCheck(self,currentuser)
        BasicAuthWithUrl(self,user_id)
        #if not UserTypeCheck(Player,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
        #    self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser))
        
        AllowedUserTypeList = [Player]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))

        level = self.request.get("level",None)
        score = self.request.get("score",None)
        pigs_killed = self.request.get("pigs_killed",None)
        
        #self.response.out.write("<br> Before player MODIFY: " + str( len( currentuser.GetLevelInfoList() ) ) )
            
        GLC.UpdatePlayerProgress(self,currentuser,level,score,pigs_killed)
        #self.response.out.write("<br> After player MODIFY: " + str( len( currentuser.GetLevelInfoList() ) ) )
        
        if SERVER_MODE:
            #if len(currentuser.GetLevelInfoList()) > 10:
                #self.response.out.write("before: " + str( len( currentuser.GetLevelInfoList() ) ) )
                #currentuser.SetLevelInfoList([LevelInfo()])
                #self.response.out.write("After: " + str(len(currentuser.GetLevelInfoList())) )

            #if len( currentuser.GetLevelInfoList() ) > 10:
                #currentuser.SetLevelInfoList([LevelInfo()])
                #self.response.out.write( "<br> HARD RESETTING BUG : " + str( len( currentuser.GetLevelInfoList() ) ))

            #self.response.out.write("<br> Before PUT: " + str( len( currentuser.GetLevelInfoList() ) ) )
            currentuser.put()#update to datastore
            #self.response.out.write("<br> After PUT: " + str( len( currentuser.GetLevelInfoList() ) ) )                           

        self.response.headers['Content-Type'] = 'application/json'
        
        jsonobj = {
            'level': str(level), 
            'score': str(score),
            'pigs_killed': str(pigs_killed),
        } 
        self.response.out.write(json.dumps(jsonobj, sort_keys = False, indent = 4 , separators = (',', ': ')) )
        self.response.set_status(200)
#player account api ends
        
#account creator account api starts    
class CreateUser(webapp2.RequestHandler): # create a user, response in json,no request body
    def post(self):
        BasicAuthWithRequest(self)

        #if not UserTypeCheck(AccountAdmin,currentuser) and  not UserTypeCheck(MasterAdmin,currentuser):
            #self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) + "Account Admin and Master Admin allowed")
        AllowedUserTypeList = [AccountAdmin]
        if MultiUserTypeCheck(AllowedUserTypeList,currentuser) == False:
            self.abort(403,'Rejected User API' +", Your user type: "+ StringUserType(currentuser) +" \n Allowed account type:" + StringMultiClassName(AllowedUserTypeList))
        
        self.response.headers['Content-Type'] = 'application/json'
        newuser,originalkey = CreatePlayerAuto()
        AddUser(self,newuser)
        
        jsonobj = {
            'user_id': str(newuser.GetUserId()), 
            'secret_key': str(originalkey),
        } 
        self.response.out.write(json.dumps(jsonobj, sort_keys = False, indent = 4 , separators = (',', ': ')) )
        self.response.set_status(201)
#account creator account api end
class DebugDeleteAccountHandler(webapp2.RequestHandler): #delete specfic user
    def post(self):
        user_id = self.request.get("userid")
        the_user = FindUser(user_id)
        if the_user == None:
            self.abort(404,"Requested user cannot be found")
            
        if SERVER_MODE:
            the_user.key.delete()
        else:
            del the_user
            
        self.response.set_status(200)
        
class DebugFlushAccountHandler(webapp2.RequestHandler):#delete all requested type of account
    def post(self):
        
        usertype = self.request.get("usertype")
        
        errormsgflag = False
        errormsg = "ERROR: "
        if usertype == '' or  usertype == None:
            errormsg += ": usertype is empty \n"
            errormsgflag = True
            
        if errormsgflag:
            self.abort(400,errormsg)

        flushlist = []
        
        if usertype == "admin":
            flushlist = GetAllAdmin()
            
            if flushlist == None or len(flushlist) == 0:
                self.abort(404,"No Admin to delete")
                
            if SERVER_MODE:
                for element in flushlist:
                    element.key.delete()
            else:
                for element in flushlist:
                    del element
        elif usertype == "player":
            flushlist = GetAllPlayer()
            
            if flushlist == None or len(flushlist) == 0:
                self.abort(404,"No Player to delete")
                
            if SERVER_MODE:
                for element in flushlist:
                    element.key.delete()
            else:
                for element in flushlist:
                    del element
        elif usertype == "user":
            flushlist = GetAllUser()
            if flushlist == None or len(flushlist) == 0:
                self.abort(404,"No User to delete")
            if SERVER_MODE:
                for element in flushlist:
                    element.key.delete()
            else:
                for element in flushlist:
                    del element            

        self.response.set_status(200)
            
class DebugAccountHandler(webapp2.RequestHandler):# create account,but not required by assignment
    def post(self):
        usertype = self.request.get("usertype")
        username = self.request.get("username")
        password = self.request.get("password")
        
        newaccount = None
        
        errormsgflag = False
        errormsg = "ERROR: "
        if usertype == '' or  usertype == None:
            errormsg += ": usertype is empty \n"
            errormsgflag = True
        
        if username == '' or  username == None:
            errormsg += ": username is empty \n"
            errormsgflag = True
        
        if password == '' or password == None:
            errormsg += " , password is empty \n"
            errormsgflag = True
                
        if errormsgflag:
            self.abort(400,errormsg)
            
        if usertype == "masteradmin":
            newaccount = MasterAdmin()
            newaccount.SetUserId(username)
            newaccount.SetSecretKey(hashlib.sha1(str(password)).hexdigest())
        elif usertype == "gameadmin":
            newaccount = GameAdmin()
            newaccount.SetUserId(username)
            newaccount.SetSecretKey(hashlib.sha1(str(password)).hexdigest())
        elif usertype == "accountadmin":
            newaccount = AccountAdmin()
            newaccount.SetUserId(username)
            newaccount.SetSecretKey(hashlib.sha1(str(password)).hexdigest())
        elif usertype == "player":
            newaccount = Player()
            newaccount.SetUserId(username)
            newaccount.SetSecretKey(hashlib.sha1(str(password)).hexdigest())

        if newaccount == None:
            self.response.write("Nothing new is created")
        else:
            AddUser(self,newaccount)
            self.response.write("<br> New Account Created: "+" <br> class name:"+ newaccount.__class__.__name__  + newaccount.StringSelf())  
            self.response.set_status(201)
            
        self.response.set_status(200)
    
class DebugUserHandler(webapp2.RequestHandler):# print out the users
    def get(self):
        if currentuser != None:
            self.response.write("Current User: " + currentuser.StringSelf()+ "<br> Type: " + StringUserType(currentuser) + "<br>")
        else:
            self.response.write("Current User: " +" NONE "+"<br>")

        user_list = []
        
        usertype = self.request.get("usertype")
        
        if usertype == "admin":
            user_list = GetAllAdmin()
        elif usertype == "player":
            user_list = GetAllPlayer()
        else:  
            user_list = GetAllUser()

        if user_list != None:
            responsestring = ""
            for index in range(len(user_list)):
                responsestring += "<br>" + " index:" + "<"+ str(index) +">"+ "<br> Type: " + StringUserType(user_list[index])+ user_list[index].StringSelf() +"<br>"
            
            self.response.write(responsestring)
        else:
            self.response.write("<br> User list is empty")
            
        self.response.set_status(200)
class SpecialDebugHandler(webapp2.RequestHandler):
    def post(self):
        BasicAuthWithRequest(self)
        self.response.out.write("<br> special debug Before anything,First check current user level list: " + str( len( currentuser.GetLevelInfoList() ) ) )

        loops = self.request.get("loops")
        if loops == '' or loops == None:
            loops = 1
        else:
            loops = int(loops)
        testlevelinfolist = []
        for count in range(loops):
            testlevelinfolist.append(LevelInfo())#pad empty levelinfo data
            
        currentuser.SetLevelInfoList(testlevelinfolist) 
        self.response.out.write("<br> special debug After appending levelinfo,Second check current user level list: " + str( len( currentuser.GetLevelInfoList() ) ) )
        currentuser.put()
        self.response.out.write( currentuser.StringSelf() )#print out the details
        self.response.out.write("<br> special debug After putting the object,third check current user level list: " + str( len( currentuser.GetLevelInfoList() ) ) )
        
    def get(self):
        BasicAuthWithRequest(self)
        self.response.out.write("<br> special debug First check current user level list: " + str( len( currentuser.GetLevelInfoList() ) ) )
        self.response.out.write( currentuser.StringSelf() )
class DebugHandler(webapp2.RequestHandler):# set debug parameters
    def get(self):
        self.response.write('Hello Debug!')
        
        servermode = self.request.get("servermode")
        if servermode == "True" or servermode == "true":  
            SetServerMode(True)
        elif servermode == "False" or servermode == "false":
            SetServerMode(False)
        else:
            SetServerMode(None)
            
        self.response.write("<br>  Current Server Mode: " + str(SERVER_MODE))
        
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

        objectcheck = currentuser
        if isinstance(objectcheck,User):
            self.response.write('<br>  currentuser is instance of User')
        if isinstance(objectcheck,Player):
            self.response.write('<br>  currentuser is instance of player')
        if isinstance(objectcheck,Admin):
            self.response.write('<br>  currentuser is instance of Admin')
        if isinstance(objectcheck,GameAdmin):
            self.response.write('<br>  currentuser is instance of GameAdmin')
        if isinstance(objectcheck,AccountAdmin):
            self.response.write('<br>  currentuser is instance of AccountAdmin')
        if isinstance(objectcheck,MasterAdmin):
            self.response.write('<br>  currentuser is instance of MasterAdmin')
        
        self.response.set_status(200)
        
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
        self.response.set_status(200)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    webapp2.Route('/special', handler = SpecialDebugHandler,name = 'SpecialDebugHandler'),
    webapp2.Route('/debug', handler = DebugHandler,name = 'DebugHandler'),
    webapp2.Route('/debug/create', handler = DebugAccountHandler,name = 'DebugAccountHandler'),
    webapp2.Route('/debug/flush', handler = DebugFlushAccountHandler,name = 'DebugFlushAccountHandler'),
    webapp2.Route('/debug/delete', handler = DebugDeleteAccountHandler,name = 'DebugDeleteAccountHandler'),
    webapp2.Route('/debug/users', handler = DebugUserHandler,name = 'DebugUserHandler'),
    webapp2.Route('/user/create', handler = CreateUser,name = 'CreateUser'),
    webapp2.Route('/user/create/', handler = CreateUser,name = 'CreateUser'),
    webapp2.Route('/user/<user_id:.+>/progress', handler = UpdateUserProgress,name = 'UpdateUserProgress'),
    webapp2.Route('/user/<user_id:.+>/progress/<level:[\d]+>', handler = GetUserProgress,name = 'GetUserProgress'),
    webapp2.Route('/user/<user_id:.+>/progress/<level:[\d]+>/', handler = GetUserProgress,name = 'GetUserProgress'),
    webapp2.Route('/user/<user_id:.+>/unlocked', handler = GetUserUnlockedLevels,name = 'GetUserUnlockedLevels'),
    webapp2.Route('/user/<user_id:.+>/unlocked/', handler = GetUserUnlockedLevels,name = 'GetUserUnlockedLevels'),
    webapp2.Route('/admin/players', handler = GetTotalPlayersNumber,name = 'GetTotalPlayersNumber'),
    webapp2.Route('/admin/players/', handler = GetTotalPlayersNumber,name = 'GetTotalPlayersNumber'),
    webapp2.Route('/admin/level/attempts', handler = GetLevelAttempts,name = 'GetLevelAttempts'),
    webapp2.Route('/admin/level/attempts/', handler = GetLevelAttempts,name = 'GetLevelAttempts'),
    webapp2.Route('/admin/level/average_score', handler = GetAverageHighestScore,name = 'GetAverageHighestScore'),
    webapp2.Route('/admin/level/average_score/', handler = GetAverageHighestScore,name = 'GetAverageHighestScore'),
    webapp2.Route('/admin/level/highest_level', handler = GetPlayerHighestLevel,name = 'GetPlayerHighestLevel'),
    webapp2.Route('/admin/level/highest_level/', handler = GetPlayerHighestLevel,name = 'GetPlayerHighestLevel'),
], debug=True)
