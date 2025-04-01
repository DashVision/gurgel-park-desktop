from models.main.UserModel import UserModel

class HomeController:
    def __init__(self):
        self.user_model = UserModel()
    
    def get_user_by_email(self, email):
        """Get user information by email"""
        return self.user_model.get_user_data(email)
    
    def toggle_sidebar(self, is_visible):
        """Toggle sidebar visibility"""
        return not is_visible 