from User import User
from Player import Player

class Admin(User):# erm regular admin
    def __init__(self, *args, **kwds):
        super(Admin, self).__init__(*args, **kwds)  

class GameAdmin(Admin):# this is admint that can only call game related api
    def __init__(self, *args, **kwds):
        super(GameAdmin, self).__init__(*args, **kwds)  

class AccountAdmin(Admin):# this is admint that can only call account creation related api
    def __init__(self, *args, **kwds):
        super(AccountAdmin, self).__init__(*args, **kwds)  

class MasterAdmin(GameAdmin,AccountAdmin,Player):# this would be me,all api allowed
    def __init__(self, *args, **kwds):
        super(MasterAdmin, self).__init__(*args, **kwds)  

    #def __init__(self,ndb_id = None,ndb_parent = None):
        #super(Player,self).__init__()# old style class cannot use super
       # Player.__init__(self,ndb_id,ndb_parent)#therefore gonna do it explictly

