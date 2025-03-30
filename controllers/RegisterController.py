from models.Users import UsersModel

class RegisterController:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

        self.createUser(self.name, self.email, self.password)

    @staticmethod
    def createUser(name, email, password):
        return UsersModel().createUser(name, email, password)