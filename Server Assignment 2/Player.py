from User import *

class LevelInfo(ndb.Model): #to describe a level information for the player data

    classname = ndb.StringProperty()
    pigs_killed = ndb.IntegerProperty()
    highest_score = ndb.IntegerProperty()
    total_attempts = ndb.IntegerProperty()
    
    inited_before = False
    
    def __init__(self, *args, **kwds):
        super(LevelInfo, self).__init__(*args, **kwds)
    def EnsureDataReady(self):
        self.SecuredInit(True,False)
    def SecuredInit(self,skip_if_inited_before,force_init):
        
        if force_init == True:
            self.Init()
            return
        
        if skip_if_inited_before == True:
            if self.inited_before == True:
                return
            

            
        if self.pigs_killed == None:
             self.pigs_killed = 0
        if self.highest_score == None:
             self.highest_score = 0
        if self.total_attempts == None:
             self.total_attempts  = 0
        if self.classname == None:
             self.classname = self.__class__.__name__ 
            
        self.inited_before = True
    def Init(self): 
        self.pigs_killed = 0
        self.highest_score = 0
        self.total_attempts  = 0
        self.classname = self.__class__.__name__
        self.inited_before = True
        
    def Populate(self,pigs_killed,highest_score,total_attempts): #set all field 
        self.pigs_killed = pigs_killed
        self.highest_score = highest_score
        self.total_attempts = total_attempts
        
    def GetClassName(self):
        self.EnsureDataReady()
        return self.__class__.__name__
    
    def StringSelf(self): #print out self information as string
        self.EnsureDataReady()
        return " <br> pigs_killed: "+ str(self.pigs_killed) + \
                " <br> highest_score: " + str(self.highest_score) + \
                " <br> total_attempts: " + str(self.total_attempts)

    def GetPigsKilled(self):
        self.EnsureDataReady()
        return self.pigs_killed
    def SetPigsKilled(self,value):
        self.EnsureDataReady()
        self.pigs_killed = value
        
    def GetHighestScore(self):
        self.EnsureDataReady()
        return self.highest_score
    def SetHighestScore(self,value):
        self.EnsureDataReady()
        self.highest_score = value
        
    def GetTotalAttempts(self):
        self.EnsureDataReady()
        return self.total_attempts
    def SetTotalAttempts(self,value):
        self.EnsureDataReady()
        self.total_attempts = value
    def IncrementTotalAttempts(self,value):
        self.EnsureDataReady()
        self.total_attempts += value

class Player(User): #to describe a player
    
    level_info_list = ndb.StructuredProperty(LevelInfo,repeated=True)
    inited_before = False
    
    def __init__(self, *args, **kwds):
        super(Player, self).__init__(*args, **kwds)
    def EnsureDataReady(self):
        self.SecuredInit(True,False)
    def SecuredInit(self,skip_if_inited_before,force_init):
        
        if force_init == True:
            self.Init()
            return
        
        if skip_if_inited_before == True:
            if self.inited_before == True:
                return
            
        if self.classname == None:
             self.classname = self.__class__.__name__ 
        if self.level_info_list == None:
            self.level_info_list  = [LevelInfo()]
            
        self.inited_before = True
            
    def Init(self):
        self.level_info_list  = [LevelInfo()]
        self.classname = self.__class__.__name__ 
        self.inited_before = True
        
    def Populate(self,user_id,secret_key,level_info_list): #set all field
        User.Populate(self,user_id,secret_key)
        
        if level_info_list != None:
            self.level_info_list = level_info_list
        
    def StringLevelInfoList(self):
        self.EnsureDataReady()
        returnstring = ""
        for index, levelinfo in enumerate(self.level_info_list):
            returnstring+= "<br>\n Index:" + str(index)+" (level)"+ str(index+1)+" :" + levelinfo.StringSelf()
        return returnstring
            
    def StringSelf(self): #print out self information as string
        self.EnsureDataReady()
        return User.StringSelf(self) + \
               " <br> level_record: " + self.StringLevelInfoList()

    def PopulateLevelRecord(self,index,pigs_killed,highest_score,total_attempts):
        self.EnsureDataReady()
        self.level_info_list[index].Populate(pigs_killed,highest_score,total_attempts)

    def PadEmptyLevelInfo(self,desire_size):
        self.EnsureDataReady()
        list_size = len(self.level_info_list)
        if desire_size <= list_size:#escape if invalid request
            return
        pad_amount = desire_size - list_size
        for i in range(pad_amount):
            self.level_info_list.append(LevelInfo())
        
    def DeleteLevelInfo(self,index):
        self.EnsureDataReady()
        del self.level_info_list[index]
    def AddLevelInfo(self,level_info):
        self.EnsureDataReady()
        self.level_info_list.append(level_info)
        
    def GetLevelUnlockedCount(self):
        self.EnsureDataReady()
        return len(self.level_info_list)
    
    def GetLevelInfo(self,index):
        self.EnsureDataReady()
        return self.level_info_list[index]
    def SetLevelInfo(self,level_info,index):
        self.EnsureDataReady()
        self.level_info_list[index] = level_info
    def GetLevelInfoList(self):
        self.EnsureDataReady()
        return self.level_info_list
    def SetLevelInfoList(self,level_record_list):
        self.level_info_list = level_record_list


    def GetLevelPigsKilled(self,index):
        self.EnsureDataReady()
        return self.level_info_list[index].GetPigsKilled()
    def SetLevelPigsKilled(self,index,value):
        self.EnsureDataReady()
        self.level_info_list[index].SetPigsKilled(value)
        
    def GetLevelHighestScore(self,index):
        self.EnsureDataReady()
        return self.level_info_list[index].GetHighestScore()
    def SetLevelHighestScore(self,index,value):
        self.EnsureDataReady()
        self.level_info_list[index].SetHighestScore(value)
        
    def GetLevelTotalAttempts(self,index):
        self.EnsureDataReady()
        return self.level_info_list[index].GetTotalAttempts()
    def SetLevelTotalAttempts(self,index,value):
        self.EnsureDataReady()
        self.level_info_list[index].SetTotalAttempts(value)
    def IncrementLevelTotalAttempts(self,index,value):
        self.EnsureDataReady()
        self.level_info_list[index].IncrementTotalAttempts(value)
