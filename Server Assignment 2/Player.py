from User import User

class LevelInfo: #to describe a level information for the player data

    def __init__(self):
        #print "Levelinfo class inited"
        self.pigs_killed = -1
        self.highest_score = -1
        self.total_attempts  = -1
        
    def Populate(self,pigs_killed,highest_score,total_attempts): #set all field 
        self.pigs_killed = pigs_killed
        self.highest_score = highest_score
        self.total_attempts = total_attempts
        
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

class Player(User): #to describe a player
    def __init__(self):
        #super(Player,self).__init__()# old style class cannot use super
        User.__init__(self)#therefore gonna do it explictly
        self.level_info_list  = []
        #print "Player class inited"
         
    def Populate(self,user_id,secret_key,level_info_list): #set all field
        User.Populate(self,user_id,secret_key)
        self.level_info_list = level_info_list
        
    def StringLevelInfoList(self):
        returnstring = ""
        for index, levelinfo in enumerate(self.level_info_list):
            returnstring+= " Index:" + str(index)+":" + levelinfo.StringSelf()
        return returnstring
            
    def StringSelf(self): #print out self information as string
        return User.StringSelf(self) + \
               " <br> level_record: " + self.StringLevelInfoList()

    def PopulateLevelRecord(self,index,pigs_killed,highest_score,total_attempts):
        self.level_info_list[index].Populate(pigs_killed,highest_score,total_attempts)
        
    def DeleteLevelInfo(self,index):
        del self.level_info_list[index]
    def AddLevelInfo(self,level_info):
        self.level_info_list.append(level_info)
        
    def GetLevelInfo(self,index):
        return self.level_info_list[index]
    def SetLevelInfo(self,level_info,index):
        self.level_info_list[index] = level_info
    def GetLevelInfoList(self):
        return self.level_info_list
    def SetLevelInfoList(self,level_record_list):
        self.level_info_list = level_record_list
