from models.auth.recovery import Recovery
from models.auth.user import User

class RecoveryController:
    def __init__(self) -> None:
        pass

    @staticmethod
    def send_recovery_code(email) -> str:
        return Recovery.send_recovery_code(email)

    @staticmethod
    def switch_password(email, new_password) -> bool:
        users_model = User()
        return users_model.update_password(email, new_password)