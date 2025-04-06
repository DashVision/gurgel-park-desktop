from models.auth.user import User

class RegisterController:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_user(name, email, password) -> any:
        return User().create_user(name, email, password)