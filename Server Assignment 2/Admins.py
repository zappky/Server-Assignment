from User import User
from Player import Player

class Admin(User):# erm regular admin
    pass

class GameAdmin(Admin):# this is admint that can only call game related api
    pass

class AccountAdmin(Admin):# this is admint that can only call account creation related api
    pass


class MasterAdmin(GameAdmin,AccountAdmin,Player):# this would be me,all api allowed
    pass
