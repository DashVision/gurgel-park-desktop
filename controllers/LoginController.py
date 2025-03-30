from models.Users import UsersModel

class LoginController:
    def __init__(self, email, password):
        self.email = email
        self.password = password

        self.verifyIfUser(self.email, self.password)

    @staticmethod
    def verifyIfUser(email, password):
        return UsersModel.readUser(email, password)
    