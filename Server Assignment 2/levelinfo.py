class LevelInfo: #to describe a level information for the player data

    def __init__(self):
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
    
