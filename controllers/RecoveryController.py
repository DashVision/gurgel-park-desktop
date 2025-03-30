from models.RecoverySenderCode import CodeSenders
from models.Users import UsersModel

class RecoveryController:
    def __init__(self, email):
        self.email = email
        self.code = self.sendCode(email)

    def sendCode(self, email):
        return CodeSenders.sendCodes(email)

    def switchPassoword(self, email, new_password):
        users_model = UsersModel()
        return users_model.updateUserPassword(email, new_password)