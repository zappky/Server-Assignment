class Player: #to describe a player
    def __init__(self):
        self.user_id = -1
        self.secret_key = -1
        self.level_record  = []
         
    def Populate(self,user_id,secret_key,level_record): #set all field 
        self.user_id = user_id
        self.secret_key = secret_key
        self.level_record = level_record
        
    def StringLevelRecord(self):
        returnstring = ""
        for index, level in enumerate(self.level_record):
            returnstring+= " Index:" + str(index)+":" + level.StringSelf()
        return returnstring
            
    def StringSelf(self): #print out self information as string
        return " <br> user_id: "+ str(self.user_id) + \
                " <br> secret_key: " + str(self.secret_key) + \
                " <br> level_record: " + self.StringLevelRecord()

    def GetUserId(self):
        return self.user_id
    def SetUserId(self,user_id):
        self.user_id = user_id
        
    def GetSecretKey(self):
        return self.secret_key
    def SetSecretKey(self,secret_key):
        self.secret_key = secret_key

    def GetLevelRecord(self):
        return self.level_record
    def SetLevelRecord(self,level_record):
        self.level_record = level_record
