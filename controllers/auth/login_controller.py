from models.auth.user import User

class LoginController:
    def __init__(self) -> None:
        pass

    @staticmethod
    def handle_user_login(email, password=None) -> any:
        return User.read_user(email, password)