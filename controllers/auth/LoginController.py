from models.auth.Users import UsersModel

class LoginController:
    def __init__(self, email, password):
        self.email = email
        self.password = password

        self.verifyUserLogin(self.email, self.password)

    @staticmethod
    def verifyUserLogin(email, password=None):
        return UsersModel.readUser(email, password)