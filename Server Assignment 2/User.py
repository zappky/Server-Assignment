class User():
    def __init__(self):
        self.user_id = "-1"
        self.secret_key = "-1"
        #self.user_id = "zappky"
        #self.secret_key = "hentai"
        #print "User class inited"
        
    def Populate(self,user_id,secret_key):
        self.user_id = user_id
        self.secret_key = secret_key
        
    def GetUserId(self):
        return self.user_id
    def SetUserId(self,user_id):
        self.user_id = user_id
        
    def GetSecretKey(self):
        return self.secret_key
    def SetSecretKey(self,secret_key):
        self.secret_key = secret_key
        
    def CheckSecretKeyIsString(self):
        return isinstance(self.secret_key,basestring)
    
    def StringUserId(self):
        return str(self.user_id)
    def StringSecretKey(self):
        if isinstance(self.secret_key,basestring):
            return self.secret_key
        else:
            try:
                return self.secret_key.hexdigest()
            except:
                return str(self.secret_key)

    def StringSelf(self): #print out self information as string
        return " <br> user_id: "+ str(self.user_id) + \
        " <br> secret_key: " + self.StringSecretKey()
