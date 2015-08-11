from User import *

class LevelInfo(ndb.Model): #to describe a level information for the player data

    classname = ndb.StringProperty()
    pigs_killed = ndb.IntegerProperty()
    highest_score = ndb.IntegerProperty()
    total_attempts = ndb.IntegerProperty()
    
    def __init__(self,ndb_id = None,ndb_parent = None):
        
        if ndb_id != None and ndb_parent != None:
            ndb.Model.__init__(self,id = ndb_id,parent = ndb_parent)
        else:
            if ndb_id == None:
                ndb.Model.__init__(self)
            else:
                ndb.Model.__init__(self,id = ndb_id)
            if ndb_parent == None:
                ndb.Model.__init__(self)
            else:
                ndb.Model.__init__(self,parent = ndb_parent)
            
        self.pigs_killed = 0
        self.highest_score = 0
        self.total_attempts  = 0
        self.classname = self.__class__.__name__ 
        
    def Populate(self,pigs_killed,highest_score,total_attempts): #set all field 
        self.pigs_killed = pigs_killed
        self.highest_score = highest_score
        self.total_attempts = total_attempts
        
    def GetClassName(self):
        return self.__class__.__name__
    
    def StringSelf(self): #print out self information as string
        return " <br> pigs_killed: "+ str(self.pigs_killed) + \
                " <br> highest_score: " + str(self.highest_score) + \
                " <br> total_attempts: " + str(self.total_attempts)

    def GetPigsKilled(self):
        return self.pigs_killed
    def SetPigsKilled(self,value):
        self.pigs_killed = value
        
    def GetHighestScore(self):
        return self.highest_score
    def SetHighestScore(self,value):
        self.highest_score = value
        
    def GetTotalAttempts(self):
        return self.total_attempts
    def SetTotalAttempts(self,value):
        self.total_attempts = value
    def IncrementTotalAttempts(self,value):
        self.total_attempts += value

class Player(User): #to describe a player
    
    level_info_list = ndb.StructuredProperty(LevelInfo,repeated=True)
    
    def __init__(self,ndb_id = None,ndb_parent = None):
        #super(Player,self).__init__()# old style class cannot use super
        User.__init__(self,ndb_id,ndb_parent)#therefore gonna do it explictly
        self.level_info_list  = [LevelInfo()] #init with the blank first level#the len of this list would be count of unlocked stages# index 0 would be level 1
        #print "Player class inited"
         
    def Populate(self,user_id,secret_key,level_info_list): #set all field
        User.Populate(self,user_id,secret_key)
        
        if level_info_list != None:
            self.level_info_list = level_info_list
        
    def StringLevelInfoList(self):
        returnstring = ""
        for index, levelinfo in enumerate(self.level_info_list):
            returnstring+= "<br>\n Index:" + str(index)+" (level)"+ str(index+1)+" :" + levelinfo.StringSelf()
        return returnstring
            
    def StringSelf(self): #print out self information as string
        return User.StringSelf(self) + \
               " <br> level_record: " + self.StringLevelInfoList()

    def PopulateLevelRecord(self,index,pigs_killed,highest_score,total_attempts):
        self.level_info_list[index].Populate(pigs_killed,highest_score,total_attempts)

    def PadEmptyLevelInfo(self,desire_size):
        list_size = len(self.level_info_list)
        if desire_size <= list_size:#escape if invalid request
            return
        pad_amount = desire_size - list_size
        for i in range(pad_amount):
            self.level_info_list.append(LevelInfo())
        
    def DeleteLevelInfo(self,index):
        del self.level_info_list[index]
    def AddLevelInfo(self,level_info):
        self.level_info_list.append(level_info)
        
    def GetLevelUnlockedCount(self):
        return len(self.level_info_list)
    
    def GetLevelInfo(self,index):
        return self.level_info_list[index]
    def SetLevelInfo(self,level_info,index):
        self.level_info_list[index] = level_info
    def GetLevelInfoList(self):
        return self.level_info_list
    def SetLevelInfoList(self,level_record_list):
        self.level_info_list = level_record_list


    def GetLevelPigsKilled(self,index):
        return self.level_info_list[index].GetPigsKilled()
    def SetLevelPigsKilled(self,index,value):
        self.level_info_list[index].SetPigsKilled(value)
        
    def GetLevelHighestScore(self,index):
        return self.level_info_list[index].GetHighestScore()
    def SetLevelHighestScore(self,index,value):
        self.level_info_list[index].SetHighestScore(value)
        
    def GetLevelTotalAttempts(self,index):
        return self.level_info_list[index].GetTotalAttempts()
    def SetLevelTotalAttempts(self,index,value):
        self.level_info_list[index].SetTotalAttempts(value)
    def IncrementLevelTotalAttempts(self,index,value):
        self.level_info_list[index].IncrementTotalAttempts(value)
