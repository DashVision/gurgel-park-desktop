from models.auth.recovery import Recovery
from models.auth.user import User

class RecoveryController:
    def __init__(self, email) -> None:
        self.email = email
        self.code = self.send_recovery_code(self.email)

    def send_recovery_code(self, email) -> str:
        return Recovery.send_recovery_code(email)

    def switch_password(self, email, new_password) -> bool:
        users_model = User()
        return users_model.update_password(email, new_password)