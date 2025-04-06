from models.auth.user import User

class RegisterController:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_user(name, email, password) -> Any:
        return User().create_user(name, email, password)